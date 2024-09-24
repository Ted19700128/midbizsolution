// plantlayout/static/plantlayout/js/update_playout.js

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('layoutCanvas');
    const context = canvas.getContext('2d');
    let isDragging = false;
    let selectedEquipment = null;

    // 레이아웃 데이터를 가져옴
    const layoutData = JSON.parse('{{ layout_data|safe }}');
    const equipments = [];

    // 레이아웃에서 설비 정보를 equipments 배열에 저장
    layoutData.plants.forEach(plant => {
        plant.units.forEach(unit => {
            unit.lines.forEach(line => {
                line.equipments.forEach(equipment => {
                    equipments.push(equipment);
                });
            });
        });
    });

    // 캔버스 이벤트 리스너 설정
    canvas.addEventListener('mousedown', function(event) {
        const rect = canvas.getBoundingClientRect();
        const mouseX = (event.clientX - rect.left);
        const mouseY = (event.clientY - rect.top);

        // 마우스 위치에서 설비 선택
        for (let equipment of equipments) {
            if (
                mouseX >= equipment.position.x &&
                mouseX <= equipment.position.x + equipment.size_width &&
                mouseY >= equipment.position.y &&
                mouseY <= equipment.position.y + equipment.size_length
            ) {
                isDragging = true;
                selectedEquipment = equipment;
                break;
            }
        }
    });

    canvas.addEventListener('mousemove', function(event) {
        if (isDragging && selectedEquipment) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = (event.clientX - rect.left);
            const mouseY = (event.clientY - rect.top);

            // 설비 위치 업데이트
            selectedEquipment.position.x = mouseX - selectedEquipment.size_width / 2;
            selectedEquipment.position.y = mouseY - selectedEquipment.size_length / 2;

            // 레이아웃 다시 그리기
            drawLayout();
        }
    });

    canvas.addEventListener('mouseup', function(event) {
        if (isDragging && selectedEquipment) {
            isDragging = false;

            // 서버로 위치 업데이트 요청
            fetch('/plantlayout/update_equipment_position/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    equipment_id: selectedEquipment.id,
                    new_x: selectedEquipment.position.x,
                    new_y: selectedEquipment.position.y
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('설비 위치가 업데이트되었습니다.');
                } else {
                    alert('업데이트에 실패했습니다.');
                }
            });
        }
    });

    function drawLayout() {
        // 레이아웃을 그리는 로직 구현
        context.clearRect(0, 0, canvas.width, canvas.height);

        // 설비 그리기
        equipments.forEach(equipment => {
            context.fillStyle = 'gray';
            context.fillRect(
                equipment.position.x,
                equipment.position.y,
                equipment.size_width,
                equipment.size_length
            );
        });
    }

    // 초기 레이아웃 그리기
    drawLayout();

    // CSRF 토큰 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
