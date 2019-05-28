console.log('hello world');

function getCurrentList() {
  var url = new URL(window.location.href);
  return (url.searchParams.get("list"));
}


let currentList = getCurrentList();
var questionDiv = document.getElementById("question");
if (questionDiv.classList.contains('blank')) {
  console.log('I should get a Q');
}
