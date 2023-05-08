//-----------Var Inits--------------
canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
cx = ctx.canvas.width / 2;
cy = ctx.canvas.height / 2;

let confetti = [];
const confettiCount = 300;
const gravity = 0.5;
const terminalVelocity = 5;
const drag = 0.075;
const colors = [
    { front: '#db4844', back: 'red' },
    { front: '#abcd58', back: '#abcd58' },
    { front: '#EFCEFA', back: '#9deacb' },
    { front: '#f6da74', back: 'yellow' },
    { front: '#f07c22', back: 'darkorange' },
    { front: '#ee92c2', back: '#E0607E' },
    { front: '#d7b4f3', back: '#C3B1E1' },
    { front: '#a2dad5', back: '#05a8aa' }];


//-----------Functions--------------
resizeCanvas = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    cx = ctx.canvas.width / 2;
    cy = ctx.canvas.height / 2;
};

randomRange = (min, max) => Math.random() * (max - min) + min;

initConfetti = () => {
    for (let i = 0; i < confettiCount; i++) {
        confetti.push({
            color: colors[Math.floor(randomRange(0, colors.length))],
            dimensions: {
                x: randomRange(10, 20),
                y: randomRange(10, 30)
            },

            position: {
                x: randomRange(0, canvas.width),
                y: canvas.height - 1
            },

            rotation: randomRange(0, 2 * Math.PI),
            scale: {
                x: 1,
                y: 1
            },

            velocity: {
                x: randomRange(-25, 25),
                y: randomRange(0, -50)
            }
        });


    }
};

//---------Render-----------
render = () => {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // add text on canvas
    ctx.font = "700 45px 'Raleway', sans-serif";
    ctx.fillStyle = "#0e1b4d";
    ctx.textAlign = "center";
    ctx.fillText(localStorage.getItem("event_name"), canvas.width / 2, canvas.height / 2 - 130);
    ctx.font = "500 25px 'Raleway', sans-serif";
    ctx.fillStyle = "#9195a2";
    ctx.textAlign = "center";
    ctx.fillText(localStorage.getItem("date"), canvas.width / 2, canvas.height / 2 - 90);

    ctx.fillStyle = "#E7191F";
    ctx.fillRect((canvas.width) / 2 - 30, canvas.height / 2 - 70, 60, 5);

    ctx.font = "400 25px 'Raleway', sans-serif";
    ctx.fillStyle = "#0e1b4d";
    ctx.textAlign = "center";
    const words = localStorage.getItem("about").split(' ');
    const maxWidth = 700;
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const width = ctx.measureText(currentLine + ' ' + word).width;
        if (width < maxWidth) {
            currentLine += ' ' + word;
        } else {
            ctx.fillText(currentLine, canvas.width / 2, canvas.height / 2 + i * 5);
            currentLine = word;
        }
    }

    ctx.fillText(currentLine, canvas.width / 2, canvas.height / 2 + words.length * 5);

    // ctx.fillText(localStorage.getItem("about"), canvas.width / 2, canvas.height / 2 - 20);



    confetti.forEach((confetto, index) => {
        let width = confetto.dimensions.x * confetto.scale.x;
        let height = confetto.dimensions.y * confetto.scale.y;

        // Move canvas to position and rotate
        ctx.translate(confetto.position.x, confetto.position.y);
        ctx.rotate(confetto.rotation);

        // Apply forces to velocity
        confetto.velocity.x -= confetto.velocity.x * drag;
        confetto.velocity.y = Math.min(confetto.velocity.y + gravity, terminalVelocity);
        confetto.velocity.x += Math.random() > 0.5 ? Math.random() : -Math.random();

        // Set position
        confetto.position.x += confetto.velocity.x;
        confetto.position.y += confetto.velocity.y;

        // Delete confetti when out of frame
        if (confetto.position.y >= canvas.height) confetti.splice(index, 1);

        // Loop confetto x position
        if (confetto.position.x > canvas.width) confetto.position.x = 0;
        if (confetto.position.x < 0) confetto.position.x = canvas.width;

        // Spin confetto by scaling y
        confetto.scale.y = Math.cos(confetto.position.y * 0.1);
        ctx.fillStyle = confetto.scale.y > 0 ? confetto.color.front : confetto.color.back;

        // Draw confetto
        ctx.fillRect(-width / 2, -height / 2, width, height);

        // Reset transform matrix
        ctx.setTransform(1, 0, 0, 1, 0, 0);
    });

    // Fire off another round of confetti
    if (confetti.length <= 10) initConfetti();

    window.requestAnimationFrame(render);
};

//---------Execution--------
initConfetti();
render();

//----------Resize----------
window.addEventListener('resize', function () {
    resizeCanvas();
});

//------------Click------------
window.addEventListener('click', function () {
    initConfetti();
});