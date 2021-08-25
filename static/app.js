let score = 0;
const words = new Set();

$("#guess-word").on("submit", submitWord);

async function submitWord(evt) {
    evt.preventDefault();
    const word = $("#word").val();
    const response = await axios({
        url: "/check-word/json",
        method: "GET",
        params: { word },
    });

    result = response.data.result;
    if (result === "ok") {
        showMessage("Added new word", "ok");
    } else if (result === "not-on-board") {
        showMessage(`${word} is not o the board`, "err");
    } else {
        showMessage(`${word} is not valid word`, "err");
    }

    updateScore(word, result);
    return result;
}

function updateScore(word, result) {
    if (result === "ok" && !words.has(word)) {
        words.add(word);
        score += word.length;
        showScore();
        showWord(word);
    }
}

function showScore() {
    $("#score").text(`Current Score: ${score}`);
}

function showWord(word) {
    $(".words").append(`<li>${word}</li>`);
}

function showMessage(msg, cls) {
    $(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
}

//timer seconds
let count = 60;

//update count every second
let timer = setInterval(async function () {
    $("#timer").text(count);
    count--;
    if (count < 0) {
        clearInterval(timer);
        $("#guess-word").hide();
        await gameOver();
    }
}, 1000);

async function gameOver() {
    const response = await axios({
        url: "/final-score",
        method: "POST",
        data: { score: score },
    });
    const highScore = response.data.highscore;
    console.log(response);
    if (response.data.brokeRecord) {
        showMessage(`New High Score ${score}`, "ok");
    } else {
        showMessage(`Your Score ${score}`, "ok");
    }

    $(".words").hide();
}
