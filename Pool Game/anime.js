$(document).ready(function() {
    let isDragging = false;
    let line = null;
    const svgContainer = $('#svg-container svg').get(0); // Direct reference to the SVG element
    const cueBallRadius = 28; // Adjust this based on the actual radius of the cue ball

    console.log("begin")
    // Function to get the cue ball's center dynamically
    function getCueBallCenter() {
        const cueBall = $('#WHITE_Ball', svgContainer);
        return {
            x: parseFloat(cueBall.attr('cx')),
            y: parseFloat(cueBall.attr('cy'))

        };
    }

    // Function to create a new line
    function createLine(x1, y1, x2, y2) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', 'black');
        line.setAttribute('stroke-width', 10);
        svgContainer.appendChild(line);
        return line;
    }

    $(document).on('mousedown', '#WHITE_Ball', function(event) {

        //Get the cueBallCenter 
        const cueBallCenter = getCueBallCenter();

        isDragging = true;
        event.preventDefault();
        // Start the line from the center of the cue ball
        line = createLine(cueBallCenter.x, cueBallCenter.y, cueBallCenter.x, cueBallCenter.y);
    });

    $(document).on('mousemove', function(event) {
        if (isDragging && line) {
            const newPos = getPosition(event, svgContainer);
            // Update the line to extend from the cue ball's center to the new position
            line.setAttribute('x2', newPos.x);
            line.setAttribute('y2', newPos.y);
        }
    });

    $(document).on('mouseup', function() {
        isDragging = false;
        if (line) {

            //Get the cueBallCenter 
            const cueBallCenter = getCueBallCenter();

            const releasePos = getPosition(event, svgContainer);
            // Calculate velocity based on the difference
            velocityX = (cueBallCenter.x - releasePos.x) * 10; 
            velocityY = (cueBallCenter.y - releasePos.y) * 10; 

            //limit of the shot velocity
            if (Math.abs(velocityX) > 10000) {
                
                if(velocityX > 0){
                    velocityX = 10000;
                }
  
                if(velocityX < 0){
                    velocityX = -10000;
                }
            }
            if (Math.abs(velocityY) > 10000) {
               
                if(velocityY > 0){
                    velocityY = 10000;
                }
          
                if(velocityY < 0){
                    velocityY = -10000;
                }
            }

            console.log(velocityX);
            console.log(velocityY);
            svgContainer.removeChild(line);
            line = null;

            $.ajax({
                url: '/cueVels',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ velocityX: velocityX, velocityY: velocityY }),
                success: function(response) {
                    console.log(response); 
                    getFramesAndAnimate();
                },
                error: function(xhr, status, error) {
                    console.error("Error making the shot:", status, error);
                }
            });
    
           
            function getFramesAndAnimate() {
                $.getJSON('/animationTable', function(data) {
                    animateSVG(data);    

       
                }).fail(function(jqxhr, textStatus, error) {
                    const err = textStatus + ", " + error;
                    console.error("Request Failed: " + err);
                });
            }

            // Your existing function to animate frames
            function animateSVG(frames) {
                const container = $('#svg-container');
                let frameIndex = 0;

                function nextFrame() {
                    if (frameIndex < frames.length) {
                        container.html(frames[frameIndex++]);
                        setTimeout(nextFrame, 125); 
                    }
                    else{
                        $.getScript('anime.js')
                    }
                }
                nextFrame();
            }
        }
    });

    //convert screen coordinates to SVG coordinates
    function getPosition(event, svgElement) {
        var point = svgElement.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        var CTM = svgElement.getScreenCTM();
        if (CTM) {
            return point.matrixTransform(CTM.inverse());
        }
        return { x: 0, y: 0 };
    }
});

