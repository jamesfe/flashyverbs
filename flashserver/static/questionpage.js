console.log('hello world');

function getCurrentList() {
  var url = new URL(window.location.href);
  return (url.searchParams.get("list"));
}

async function getQuestionByList(listId) {
  /* Get a question and return it. */
  let request = await fetch(new Request(`/list/${listId}/`));
  if (request.status !== 200) {
    console.log('error.');
  }
  return (await request.json())
}

function getQuestionDOM() {
  /* Get the DOM object where we put the question. */
  return (document.getElementById("question"));
}

function setQuestion(q) {
  /* Update the DOM with a new question. */
  getQuestionDOM().innerHTML = q.q;
  getQuestionDOM().classList.remove('blank');
  getQuestionDOM().classList.add('filled');
}

function answerQuestion() {
  /* Answer the question and handle what happens next:
   * 1. Send the answer to the server, where it's logged
   * 2. Retrieve a new answer
   * 3. Clear the DOM and paint the relevant elements
   * 4. Return, we wait for another user action. */
  console.log('answering');
}

async function introductoryCheck() {
  /* Is this the right way to use async/await? I am open to suggestions. */
  let currentList = getCurrentList();
  let questionDiv = getQuestionDOM();
  if (questionDiv.classList.contains('blank')) {
    /* If there is nothing in the question box, we should get a question. */
    let newQuestion = await getQuestionByList(currentList);
    setQuestion(newQuestion);
  }
}
introductoryCheck();
