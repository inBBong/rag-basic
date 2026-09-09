const questionInput = document.getElementById("question");
const askButton = document.getElementById("ask-button");
const resultBox = document.getElementById("result");
const pathBox = document.getElementById("path");
const answerBox = document.getElementById("answer");
const sourcesBox = document.getElementById("sources");
const sourcesLabel = document.getElementById("sources-label");
const loadingBox = document.getElementById("loading");
const errorBox = document.getElementById("error");

let history = [];
const KEEP_TURNS = 3;

// 클릭할 때 ask()를 실행하도록 연결합니다. 지금 호출하는 것은 아닙니다.
askButton.addEventListener("click", ask);

// 키를 누를 때 Enter인지 확인하도록 연결합니다.
questionInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    // 현재 입력창의 질문으로 답변 요청을 시작합니다.
    ask();
  }
});

// 각 예시 버튼에 입력창을 채우고 질문을 보내는 동작을 연결합니다.
document.querySelectorAll(".example").forEach(function (button) {
  // 클릭할 때 아래 처리를 실행하도록 연결합니다. 지금 호출하는 것은 아닙니다.
  button.addEventListener("click", function () {
    questionInput.value = button.textContent;
    // 현재 입력창의 질문으로 답변 요청을 시작합니다.
    ask();
  });
});

// 질문을 서버로 보내고, 스트리밍 메시지가 완성될 때마다 onEvent에 넘깁니다.
async function askServer(question, onEvent) {
  // 서버에 요청을 보내고 응답이 올 때까지 이 함수의 다음 처리를 기다립니다.
  const response = await fetch("/ask/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question, history: history }),
  });

  if (!response.ok) {
    throw new Error("서버가 " + response.status + " 를 돌려주었습니다.");
  }

  // 응답을 조각씩 읽을 준비를 합니다.
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    // 다음 네트워크 조각을 기다려 읽습니다.
    const chunk = await reader.read();
    if (chunk.done) {
      break;
    }

    // 조각을 이어 붙이고, 빈 줄까지 도착한 메시지만 나눕니다.
    buffer += decoder.decode(chunk.value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop();

    parts.forEach(function (part) {
      if (part.startsWith("data: ")) {
        // 완성된 메시지 한 건을 화면 처리 함수에 넘깁니다.
        onEvent(JSON.parse(part.slice(6)));
      }
    });
  }
}

// 완료된 실행 단계를 흐름 표시줄에 하나 붙입니다.
function addNode(name, route) {
  const arrow = pathBox.children.length > 0 ? '<span class="arrow">→</span>' : "";
  pathBox.insertAdjacentHTML("beforeend", `${arrow}<span class="node ${route}">${name}</span>`);
}

// 검색 근거 한 건을 보여줄 HTML 문자열을 만듭니다.
function sourceRow(source) {
  const lines = source.content.split("\n");
  return `
    <div class="source">
      <div class="source-head">${source.source_id} · 유사도 ${source.score.toFixed(3)}</div>
      <div class="source-body">${escapeHtml(lines[0])} — ${escapeHtml(lines[1] || "")}</div>
    </div>`;
}

// 검색 근거 목록을 화면에 표시합니다.
function drawSources(sources) {
  sourcesLabel.textContent = "근거로 삼은 글 " + sources.length + "개";
  // 근거마다 sourceRow를 호출해 HTML을 만들고, 하나로 이어 붙입니다.
  sourcesBox.innerHTML = sources.map(sourceRow).join("");
}

// DB 도구가 돌려준 결과 목록을 화면에 표시합니다.
function drawToolResult(rows) {
  sourcesLabel.textContent = "DB 에서 가져온 결과 " + rows.length + "건";
  sourcesBox.innerHTML = rows
    .map(
      (row) => `
    <div class="source">
      <div class="source-body">${escapeHtml(JSON.stringify(row))}</div>
    </div>`,
    )
    .join("");
}

// 새로 받은 답변 조각을 기존 답변 뒤에 붙입니다.
function addPiece(text) {
  answerBox.textContent += text;
}

// 최종 답변과 대화 기록을 정리하고, 경로에 맞는 근거를 표시합니다.
function drawDone(result) {
  answerBox.textContent = result.answer;

  // 다음 질문에 함께 보낼 수 있도록 이번 대화를 기록합니다.
  history.push({ question: result.question, answer: result.answer });
  history = history.slice(-KEEP_TURNS);

  if (result.route === "tool") {
    // tool 경로에서 받은 DB 결과를 그립니다.
    drawToolResult(result.tool_result);
  } else {
    // rag 경로에서 찾은 문서 근거를 그립니다.
    drawSources(result.sources);
  }
}

// 지정한 화면 요소를 보이게 합니다.
function show(element) {
  element.classList.remove("hidden");
}

// 지정한 화면 요소를 감춥니다.
function hide(element) {
  element.classList.add("hidden");
}

// 입력한 질문을 읽고, 요청부터 진행 표시와 결과 처리까지 묶어 실행합니다.
async function ask() {
  const question = questionInput.value.trim();
  if (!question) {
    return;
  }

  pathBox.innerHTML = "";
  answerBox.textContent = "";
  sourcesBox.innerHTML = "";
  sourcesLabel.textContent = "근거";
  // 이 요소를 화면에 표시합니다.
  show(resultBox);

  // 이 요소를 화면에서 감춥니다.
  hide(errorBox);
  // 이 요소를 화면에 표시합니다.
  show(loadingBox);
  askButton.disabled = true;

  try {
    // 질문을 보내고, 아래 함수를 메시지가 올 때마다 실행하도록 전달합니다.
    await askServer(question, function (event) {
      if (event.type === "node") {
        // node 메시지이므로 완료된 단계를 화면에 붙입니다.
        addNode(event.name, event.route);
      } else if (event.type === "piece") {
        // piece 메시지이므로 답변 조각을 이어 붙입니다.
        addPiece(event.text);
      } else {
        // 완료 메시지를 받아 최종 답변과 근거를 정리합니다.
        drawDone(event);
      }
    });
  } catch (problem) {
    errorBox.textContent = "문제가 생겼습니다. " + problem.message;
    // 이 요소를 화면에 표시합니다.
    show(errorBox);
    // 이 요소를 화면에서 감춥니다.
    hide(resultBox);
  }

  // 이 요소를 화면에서 감춥니다.
  hide(loadingBox);
  askButton.disabled = false;
}