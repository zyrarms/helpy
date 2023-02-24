let currentChat = 1;

epds = {
  1: {
    question: "Little interest or pleasure in doing things?",
    0: "Not at all",
    1: "Several days",
    2: "More than half the days",
    3: "Nearly everyday",
  },
  2: {
    question: "Feeling down, depressed, or hopeless?",
    
    0: "Not at all",
    1: "Several days",
    2: "More than half the days",
    3: "Nearly everyday",
  },
  3: {
    question: "Trouble falling or staying asleep, or sleeping too much?",
    3: "Not at all",
    2: "Several days",
    1: "More than half the days",
    0: "Nearly everyday",
  },
  4: {
    question: "Feeling tired or having little energy?",
    0: "Not at all",
    1: "Several days",
    2: "More than half the days",
    3: "Nearly everyday",
  },
  5: {
    question: "Poor appetite or overeating?",
    3: "Not at all",
    2: "Several days",
    1: "More than half the days",
    0: "Nearly everyday",
  },
  6: {
    question: "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
    3: "Not at all",
    2: "Several days",
    1: "More than half the days",
    0: "Nearly everyday",
  },
  7: {
    question: "Trouble concentrating on things, such as reading the newspaper or watching television?",
    3: "Not at all",
    2: "Several days",
    1: "More than half the days",
    0: "Nearly everyday",
  },
  8: {
    question: "Moving or speaking so slowly that other people could have noticed? Or so fidgety or restless that you have been moving a lot more than usual?",
    3: "Not at all",
    2: "Several days",
    1: "More than half the days",
    0: "Nearly everyday",
  },
  9: {
    question: "Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?",
    3: "Not at all",
    2: "Several days",
    1: "More than half the days",
    0: "Nearly everyday",
  },
};

let epdsData = [];

elements = document.getElementsByClassName("preset-chat");
presetWrapper = document.querySelector(".chat_preset");

enterPreset = (e) => {
  epdsData.splice(currentChat - 1, 1, parseInt(e.target.id));
  document.querySelector(".chat_input").firstElementChild.value =
    e.target.textContent;
};

changeChatPreset();

function changeChatPreset() {
  if (currentChat <= 9) {
    elements[0].innerText = epds[currentChat][0];
    elements[1].innerText = epds[currentChat][1];
    elements[2].innerText = epds[currentChat][2];
    elements[3].innerText = epds[currentChat][3];

    elements[0].id = 0;
    elements[1].id = 1;
    elements[2].id = 2;
    elements[3].id = 3;
  } else {
    presetWrapper.remove();
    // presetWrapper.style.display = 'none';
  }

}

elements[0].addEventListener("click", enterPreset);
elements[1].addEventListener("click", enterPreset);
elements[2].addEventListener("click", enterPreset);
elements[3].addEventListener("click", enterPreset);

class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    // show or hides the box
    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }


    currentChat++;
    if (currentChat <= 9) {
      console.log(currentChat)
    } else {
      let sum = 0;
      for (let data of epdsData) {
        sum += data;
      }
      epdsData.splice(currentChat, 1, sum);

      if (currentChat <= 10) {
        console.log(epdsData)
        fetch("http://127.0.0.1:5000/predict_epds", {
          method: "POST",
          body: JSON.stringify({ message: epdsData }),
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((r) => r.json())
          .then((r) => {
            let msg2 = { name: "Sanitybot", message: r.answer };
            this.messages.push(msg2);
            // TODO: updated the link
            this.messages.push({ name: "Sanitybot", message: "You can download the detailed version of the assessment. <a href='http://localhost:5000/file/AssessmentResult.docx'>Click here</a>" })
            msg2 = { name: "Sanitybot", message: "Do you have any questions? I will be glad to answer all your queries." };
            this.messages.push(msg2);
            // presetWrapper.style.display = 'flex';
            // elements[0].innerText = "Yes"
            // elements[1].innerText = "No"
            // elements[2].style.display = 'none'
            // elements[3].style.display = 'none'
            this.updateChatText(chatbox);
            textField.value = "";
          })
          .catch((error) => {
            console.error("Error:", error);
            this.updateChatText(chatbox);
            textField.value = "";
          });
      } else {
        fetch('http://127.0.0.1:5000/predict', {
          method: 'POST',
          body: JSON.stringify({ message: text1 }),
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json'
          },
        })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sanitybot", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

          }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
      }
    }

    console.log(epdsData);
    changeChatPreset();



    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    if (currentChat <= 9) {
      let msg2 = { name: "Sanitybot", message: epds[currentChat]["question"] };
      this.messages.push(msg2);
    }


    this.updateChatText(chatbox);
    textField.value = "";


  }

  updateChatText(chatbox) {
    var html = "";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item, index) {
        if (item.name === "Sanitybot") {
          html +=
            '<div class="messages__item messages__item--visitor">' +
            item.message +
            "</div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();

// FOR DARK AND LIGHT MODE
var toggle_btn;
var wrapper;
var hamburger_menu;

function declare() {
  toggle_btn = document.querySelector(".toggle-btn");
  wrapper = document.querySelector(".wrapper");
  hamburger_menu = document.querySelector(".hamburger");
}

declare();

const main = document.querySelector("main");

let dark = false;

function toggleAnimation() {
  // Clone the wrapper
  dark = !dark;
  let clone = wrapper.cloneNode(true);
  if (dark) {
    clone.classList.remove("light");
    clone.classList.add("dark");
  } else {
    clone.classList.remove("dark");
    clone.classList.add("light");
  }

  clone.classList.add("copy");
  main.appendChild(clone);

  clone.addEventListener("animationend", () => {
    wrapper.remove();
    clone.classList.remove("copy");
    // Reset Variables
    declare();
    events();
  });
}

/*==================== Toggle Event ====================*/
function events() {
  toggle_btn.addEventListener("click", toggleAnimation);
  hamburger_menu.addEventListener("click", () => {
    wrapper.classList.toggle("active");
  });
}

events();

// =----------------------------------
changeChatPreset();
