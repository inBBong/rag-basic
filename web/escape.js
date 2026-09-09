// 받은 값을 HTML 코드가 아닌 글자로 표시하도록 특수문자를 바꿉니다.
function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}