// plantlayout/static/plantlayout/js/layout.js

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('layoutCanvas');
    const context = canvas.getContext('2d');

    // 줌 기능 변수
    let zoomScale = 1;
    let originx = 0;
    let originy = 0;

    // 스케일링 계산
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    // 최대 공장 크기 계산
    let maxPlantWidth = 0;
    let maxPlantLength = 0;
    layoutData.plants.forEach(plant => {
        if (plant.width > maxPlantWidth) maxPlantWidth = plant.width;
        if (plant.length > maxPlantLength) maxPlantLength = plant.length;
    });

    // 픽셀당 할당 길이 계산
    const scaleX = (canvasWidth * 0.8) / maxPlantWidth;
    const scaleY = (canvasHeight * 0.8) / maxPlantLength;
    const initialScale = Math.min(scaleX, scaleY);

    // 줌 인/아웃 기능 구현
    canvas.addEventListener('wheel', function(event) {
        event.preventDefault();
        const mousex = event.offsetX;
        const mousey = event.offsetY;
        const wheel = event.deltaY < 0 ? 1 : -1;
        const zoom = Math.exp(wheel * 0.1);

        context.translate(originx, originy);
        context.scale(zoom, zoom);
        context.translate(
            -(mousex / zoomScale + originx - mousex / (zoomScale * zoom)),
            -(mousey / zoomScale + originy - mousey / (zoomScale * zoom))
        );

        originx = (mousex / zoomScale + originx - mousex / (zoomScale * zoom));
        originy = (mousey / zoomScale + originy - mousey / (zoomScale * zoom));
        zoomScale *= zoom;

        drawLayout();
    });

    // 레이아웃 그리기 함수
    function drawLayout() {
        // 캔버스 초기화
        context.clearRect(0, 0, canvas.width, canvas.height);

        context.save();
        context.scale(zoomScale, zoomScale);

        layoutData.plants.forEach(function(plant) {
            context.save();
            context.scale(initialScale, initialScale);

            // 공장 그리기
            context.strokeStyle = 'black';
            context.lineWidth = 2 / initialScale;
            context.strokeRect(0, 0, plant.width, plant.length);

            // 공장명 및 층 표시
            context.font = `${16 / initialScale}px Arial`;
            context.fillStyle = 'black';
            context.fillText(`${plant.name} ${plant.floor}층`, 10, 20 / initialScale);

            // 구역 그리기
            plant.units.forEach(function(unit) {
                context.strokeStyle = 'blue';
                context.lineWidth = 2 / initialScale;
                context.strokeRect(
                    unit.start_point.x,
                    unit.start_point.y,
                    unit.end_point.x - unit.start_point.x,
                    unit.end_point.y - unit.start_point.y
                );

                // 라인 그리기
                unit.lines.forEach(function(line) {
                    context.strokeStyle = 'green';
                    context.lineWidth = 2 / initialScale;
                    context.setLineDash([5 / initialScale, 5 / initialScale]);
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
                        context.font = `${12 / initialScale}px Arial`;
                        context.fillText(
                            equipment.equipment_number,
                            equipment.position.x + 5,
                            equipment.position.y + 15 / initialScale
                        );
                    });
                });
            });

            context.restore();
        });

        context.restore();
    }

    // 초기 레이아웃 그리기
    drawLayout();
});
