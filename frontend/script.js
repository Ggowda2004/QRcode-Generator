let currentType = "link";

const inputArea = document.getElementById("inputArea");
const buttons = document.querySelectorAll(".tabs button");

const BASE_URL = "https://qrcode-generator-18jm.onrender.com/api/v1/qr";

/* SWITCH TABS */
function setType(event, type) {
  currentType = type;

  buttons.forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");

  switch(type) {

    case "url":
      inputArea.innerHTML = `<textarea id="url" placeholder="Enter url"></textarea>`;
      break;

    case "email":
      inputArea.innerHTML = `<input id="email" placeholder="Enter email">`;
      break;

    case "phone":
      inputArea.innerHTML = `
        <div class="phone-row">
          <input id="phone" placeholder="Phone number">
        </div>
      `;
      break;

    case "text":
      inputArea.innerHTML = `<textarea id="text" placeholder="Enter text"></textarea>`;
      break;

    case "vcard":
      inputArea.innerHTML = `
        <input id="first_name" placeholder="First Name">
        <input id="last_name" placeholder="Last Name">
        <input id="phone" placeholder="Phone">
        <input id="address" placeholder="Address">
      `;
      break;

    case "wifi":
      inputArea.innerHTML = `
        <select id="security">
          <option>WPA</option>
          <option>WPA2</option>
          <option>WPA3</option>
        </select>
        <input id="ssid" placeholder="SSID">
        <input id="password" placeholder="Password">
      `;
      break;
  }
  // Hide QR when switching type
  const img = document.getElementById("qrImage");
  img.style.display = "none";
  img.src = "";

  const dl = document.getElementById("downloadBtn");
  dl.style.display = "none";
  dl.href = "";
}

setType({target: buttons[0]}, "url");

/* GENERATE QR */
async function generateQR() {

  let endpoint = "";
  let payload = {};

  try {

    switch(currentType) {

      case "url":
        endpoint = "/url";
        payload = {
          url: document.getElementById("url").value
        };
        break;

      case "email":
        endpoint = "/mail";
        payload = {
          email: document.getElementById("email").value
        };
        break;

      case "phone":
        endpoint = "/phone";
        payload = {
          number: document.getElementById("phone").value
        };
        break;

      case "text":
        endpoint = "/text";
        payload = {
          text: document.getElementById("text").value
        };
        break;

      case "vcard":
        endpoint = "/vcard";
        payload = {
          first_name: document.getElementById("first_name").value,
          last_name: document.getElementById("last_name").value,
          phone: document.getElementById("phone").value,
          address: document.getElementById("address").value
        };
        break;

      case "wifi":
        endpoint = "/wifi";
        payload = {
          security: document.getElementById("security").value,
          ssid: document.getElementById("ssid").value,
          password: document.getElementById("password").value
        };
        break;
    }

    const res = await fetch(BASE_URL + endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const error = await res.json();
      console.log("Backend error:", error);
      alert(JSON.stringify(error, null, 2));
      return;
    }

    const blob = await res.blob();
    displayImage(blob);

  } catch (err) {
    console.error(err);
    alert("Something went wrong.");
  }
}

/* DISPLAY IMAGE */
function displayImage(blob) {
  const imgUrl = URL.createObjectURL(blob);

  const img = document.getElementById("qrImage");
  img.src = imgUrl;
  img.style.display = "block";

  const dl = document.getElementById("downloadBtn");
  dl.href = imgUrl;
  dl.style.display = "inline";
}

/* CUSTOM QR PAGE REDIRECT */
function goCustom() {
  window.location.href = "custom-qr.html";
}
