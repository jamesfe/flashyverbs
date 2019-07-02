var currentQuestion = -1;

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
  currentQuestion = q.q_id;
  getQuestionDOM().innerHTML = q.q;
  getQuestionDOM().classList.remove('blank');
  getQuestionDOM().classList.add('filled');
}

async function submitAnswer() {
  let inputAnswer = document.getElementById("answer_input").value.trim();
  if ((currentQuestion === -1) || (inputAnswer.length === 0)) {
    console.log('no answer or no set question');
    return undefined;
    // TODO: We should throw an error here and flash the input box red
  }
  payload = {
    answer: inputAnswer,
    q_id: currentQuestion,
  }

  let listId = getCurrentList()
  let request = await fetch(new Request(`/list/${listId}/`, {
    method: 'POST',
    body: JSON.stringify(payload)}));

  return await request.json();
}

async function answerQuestion() {
  /* Answer the question and handle what happens next:
   * 1. Send the answer to the server, where it's logged
   * 2. Retrieve a new question
   * 3. Clear the DOM and paint the relevant elements
   * 4. Display some relevant feedback for the user (green/red) and setTimeout to fade it
   * 5. Return, we wait for another user action. */
  let answerResponse = await submitAnswer();
  console.log('answer reponse ', answerResponse);
  // 1.
  let newQuestion = await getQuestionByList(getCurrentList());
  // 2.
  setQuestion(newQuestion);
  // 3.
  let answerClass = 'right';

  /* Make DOM updates to the feedback box. I'm sure there is a clever way to do this
   * but this code seems more transparent to me. */
  let feedbackSpace = document.getElementById('answer');
  feedbackSpace.classList.remove('blank');
  if (!answerResponse.correct) {
    feedbackSpace.classList.add('wrong');
    feedbackSpace.classList.remove('right');
  } else {
    feedbackSpace.classList.add('wrong');
    feedbackSpace.classList.remove('right');
  }
  feedbackSpace.hidden = false;
  /* Finished making DOM updates */


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
  let feedbackSpace = document.getElementById('answer');
  if (feedbackSpace.classList.contains('blank')) {
    feedbackSpace.hidden = true;
  }
}
introductoryCheck();
