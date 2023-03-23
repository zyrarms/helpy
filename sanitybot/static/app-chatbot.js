let currentChat = 1;
let is_done = false;

epds = {
  1: {
    question: "Are you feeling despair when you are doing something that you typically enjoy??",
    0: "Nope, not at all.",
    1: "Yes, I feel that way",
    2: "Almost an entire day",
    3: "Consistently day after day",
  },
  2: {
    question: "I've noticed that you've been isolating yourself and feeling down more lately and may be experiencing feelings of hopelessness. Have you noticed any changes or improvements in your mood and outlook?",
    0: "No, I dont noticed any changes",
    1: "Yes, I experiecing that kind of feeling.",
    2: "Sometimes I feel that way and I noticed it.",
    3: "I'm worried i felt that way every day.",
  },
  3: {
    question: "But how was your sleeping schedule lately? How was your sleep been, and have you been experiencing any difficulty falling or staying asleep? You seem like you're going through a tough time.",
    0: "My sleep schedule is okay.",
    1: "Its not good lately",
    2: "Its hard for me to get a sleep.",
    3: "I'm having difficulty getting to sleep.",
  },
  4: {
    question: "It will appears in feeling tired and low on energy. So, have you noticed any patterns or triggers that might be contributing to your fatigue like particular reasons for your lack of energy, such as stress or changes in your routine?",
    0: "Not even a little bit",
    1: "Yes, sometimes.",
    2: "Half of the day I almost faint",
    3: "What to do if I feel fatigue everday",
  },
  5: {
    question: "Oh I see. Somehow I sense that you may be experiencing feelings of shame or self-blame. Is there anything thats been weighing heavily on your mind, such as past mistakes or current challenges that can me you feel of failure or disappointment anything in particular that has been contributing to these thoughts?",
    0: "No, I dont have any thoughts like that.",
    1: "Yes, sometimes I feel anxious about that.",
    2: "I often find myself dwelling on the mistakes I've made before.",
    3: "My past mistakes still weigh heavily on my mind.",
  },
  6: {
    question: "Oh, but one thing that might help to avoid bad thoughts is to focus. So, how is your experience uncontrollable worrying thoughts that seem to dominate your mind, and does it affect your daily life and activities?",
    0: "Im not experiencing any of those",
    1: "Quite a few days I guess",
    2: "I spend about half the day feeling that way.",
    3: "I'm anxious about experiencing this feeling every day",
  },
  7: {
    question: "I understand. But have you noticed that you frequently have an overwhelming sense of fear or dread, as if something terrible is about to happen, despite there being no logical reason for it and interfere it with your ability to function normally in your daily life?",
    0: "I dont think so",
    1: "Yes, A couple of days",
    2: "The majority of the day, I am in this state.",
    3: "Yes, Every single day.",
  },
  8: {
    question: "Its important to remember that we all make mistakes and experience setbacks, and that its possible to learn and grow from these experiences. Do you feel having difficulty focusing on certain things?",
    0: "Nope, not at all.",
    1: "Once in a while",
    2: "Yes, almost the whole day.",
    3: "Yes, Practically in every day.",
  },
  9: {
    question: "Well, just remember that it's okay to make mistake and learn form it. Is there any chance that you have thoughts of harming yourself or feeling like you would be better off not living? If so better to address these thoughts as soon as possible and seek professional help, such as talking to a therapist or counselor, to get the support and guidance you need. Remember, you are not alone and there is help available to you.",
    0: "No, I never think that way.",
    1: "Somedays, it taking part of my mind",
    2: "It seems like I'm feeling this way all day long.",
    3: "I think im just anxious so I think this kind of stuff.",
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

function toggleChatPreset(hide) {
  const chatPresetDiv = document.querySelector('.chat_preset');
  if (hide) {
    chatPresetDiv.style.display = 'none';
  } else {
    is_done = true;
    chatPresetDiv.style.display = '';
  }
}

toggleChatPreset(true);

class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector('.chatbox__button'),
      chatBox: document.querySelector('.chatbox__support'),
      sendButton: document.querySelector('.send__button')
    }

    this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener('click', () => this.toggleState(chatBox))

    sendButton.addEventListener('click', () => this.onSendButton(chatBox))

    const node = chatBox.querySelector('input');
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox)
      }
    })
  }

  toggleState(chatbox) {
    this.state = !this.state;

    // show or hides the box
    if (this.state) {
      chatbox.classList.add('chatbox--active')
    } else {
      chatbox.classList.remove('chatbox--active')
    }
  }
  onSendButton(chatbox) {

    var textField = chatbox.querySelector('input');
    let text1 = textField.value
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 }
    this.messages.push(msg1);

    // if (text1.toLowerCase().includes("yes") || text1.toLowerCase().includes("okay") || text1.toLowerCase().includes("sure")) {
    //   this.epds_chatbot(chatbox)
    // } else 
    if (text1.toLowerCase().includes("thanks") || text1.toLowerCase().includes("thank you") || text1.toLowerCase().includes("thank you!")) {
      let msg2 = { name: "Sanitybot", message: "Wait up! May I ask you something if... " };
      let msg3 = { name: "Sanitybot", message: "Lately did you have a little interest or pleasure in doing things?" };
      this.messages.push(msg2);
      this.messages.push(msg3);
      this.updateChatText(chatbox)
      textField.value = ''
      is_done = true;
      // show the chat_preset
      toggleChatPreset(false);
    }

    if (is_done) {

      this.epds_chatbot(chatbox);
    } else {
      // hide the chat_preset
      toggleChatPreset(true);
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

  epds_chatbot(chatbox) {

    var textField = chatbox.querySelector('input');
    let text1 = textField.value
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
            this.messages.push({ name: "Sanitybot", message: "Simply go to this page to <a href='/result'>view result.</a>" })

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


    if (currentChat <= 9) {
      let msg2 = { name: "Sanitybot", message: epds[currentChat]["question"] };
      this.messages.push(msg2);
    }


    this.updateChatText(chatbox);
    textField.value = "";
  }

  updateChatText(chatbox) {
    var html = '';
    this.messages.slice().reverse().forEach(function (item, index) {
      if (item.name === "Sanitybot") {
        html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
      }
      else {
        html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
      }
    });
    const chatmessage = chatbox.querySelector('.chatbox__messages');
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
  console.log("Dark mode")
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
