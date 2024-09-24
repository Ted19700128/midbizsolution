// plantlayout/static/plantlayout/js/create_playout.js

document.addEventListener('DOMContentLoaded', function() {
    const createConfirmButton = document.getElementById('create_confirm');
    const form = document.querySelector('form');

    createConfirmButton.addEventListener('click', function(event) {
        event.preventDefault();

        // 폼 데이터를 가져옴
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const csrfToken = getCookie('csrftoken');

        // 서버로 데이터 전송하여 레이아웃 업데이트
        fetch('/plantlayout/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 좌측 레이아웃 뷰를 업데이트하는 함수 호출
                updateLayoutView(data.layout);
            } else {
                alert('레이아웃 생성에 실패했습니다.');
            }
        });
    });

    function updateLayoutView(layoutData) {
        // 레이아웃을 그리는 로직 구현
        // layoutData를 사용하여 좌측 레이아웃 뷰를 업데이트합니다.
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

