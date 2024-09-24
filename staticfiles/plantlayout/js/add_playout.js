// plantlayout/static/plantlayout/js/add_playout.js

document.addEventListener('DOMContentLoaded', function() {
    const addConfirmButton = document.getElementById('add_confirm');
    const form = document.querySelector('form');

    addConfirmButton.addEventListener('click', function(event) {
        event.preventDefault();

        // 폼 데이터를 가져옴
        const formData = new FormData(form);
        const csrfToken = getCookie('csrftoken');

        // 서버로 데이터 전송하여 요소 추가
        fetch('/plantlayout/add/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 좌측 레이아웃 뷰를 업데이트하는 함수 호출
                updateLayoutView(data.layoutData);
            } else {
                alert('요소 추가에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function updateLayoutView(layoutData) {
        // 레이아웃 캔버스 가져오기
        const canvas = document.getElementById('layoutCanvas');
        const context = canvas.getContext('2d');

        // 캔버스 초기화
        context.clearRect(0, 0, canvas.width, canvas.height);

        // 레이아웃 데이터를 기반으로 요소 그리기
        layoutData.plants.forEach(function(plant) {
            // 공장 그리기
            context.strokeStyle = 'black';
            context.lineWidth = 2;
            context.strokeRect(0, 0, plant.width, plant.length);

            // 공장명 및 층 표시
            context.font = '16px Arial';
            context.fillStyle = 'black';
            context.fillText(`${plant.name} ${plant.floor}층`, 10, 20);

            // 구역 그리기
            plant.units.forEach(function(unit) {
                context.strokeStyle = 'blue';
                context.lineWidth = 2;
                context.strokeRect(
                    unit.start_point.x,
                    unit.start_point.y,
                    unit.end_point.x - unit.start_point.x,
                    unit.end_point.y - unit.start_point.y
                );

                // 라인 그리기
                unit.lines.forEach(function(line) {
                    context.strokeStyle = 'green';
                    context.lineWidth = 2;
                    context.setLineDash([5, 5]);
                    context.strokeRect(
                        line.start_point.x,
                        line.start_point.y,
                        line.end_point.x - line.start_point.x,
                        line.end_point.y - line.start_point.y
                    );
                    context.setLineDash([]);

                    // 설비 그리기
                    line.equipments.forEach(function(equipment) {
                        context.fillStyle = 'gray';
                        context.fillRect(
                            equipment.position.x,
                            equipment.position.y,
                            equipment.size_width,
                            equipment.size_length
                        );

                        // 설비 번호 표시
                        context.fillStyle = 'white';
                        context.font = '12px Arial';
                        context.fillText(
                            equipment.equipment_number,
                            equipment.position.x + 5,
                            equipment.position.y + 15
                        );
                    });
                });
            });
        });
    }

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
