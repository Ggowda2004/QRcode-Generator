let currentType = "link";

const inputArea = document.getElementById("inputArea");
const buttons = document.querySelectorAll(".tabs button");

/* SWITCH TABS */
function setType(event, type) {

  currentType = type;

  buttons.forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");

  switch(type) {

    case "link":
      inputArea.innerHTML = `<textarea id="link" placeholder="Enter link"></textarea>`;
      break;

    case "email":
      inputArea.innerHTML = `<input id="email" placeholder="Enter email">`;
      break;

    case "phone":
      inputArea.innerHTML = `
        <div class="phone-row">
          <select id="countryCode" class="smooth-select">
            <option value="+91" selected>🇮🇳 +91</option>
            <option value="+1">🇺🇸 +1</option>
            <option value="+44">🇬🇧 +44</option>
            <option value="+61">🇦🇺 +61</option>
            <option value="+81">🇯🇵 +81</option>
          </select>
          <input id="phone" placeholder="Phone number">
        </div>
      `;
      break;

    case "text":
      inputArea.innerHTML = `<textarea id="text" placeholder="Enter text"></textarea>`;
      break;

    case "vcard":
      inputArea.innerHTML = `
        <input id="first" placeholder="First Name">
        <input id="last" placeholder="Last Name">
        <input id="vphone" placeholder="Phone">
        <input id="address" placeholder="Address">
      `;
      break;

    case "wifi":
      inputArea.innerHTML = `
        <select id="security" class="smooth-select">
          <option>WPA</option>
          <option>WPA2</option>
          <option>WPA3</option>
        </select>
        <input id="ssid" placeholder="SSID">
        <input id="password" placeholder="Password">
      `;
      break;
  }
}

setType({target: buttons[0]}, "link");

/* GENERATE QR */
async function generateQR() {

  let finalData = "";

  switch(currentType) {

    case "link":
      finalData = document.getElementById("link").value;
      break;

    case "email":
      finalData = "mailto:" + document.getElementById("email").value;
      break;

    case "phone":
      finalData = "tel:" +
        document.getElementById("countryCode").value +
        document.getElementById("phone").value;
      break;

    case "text":
      finalData = document.getElementById("text").value;
      break;

    case "vcard":
      finalData =
`BEGIN:VCARD
VERSION:3.0
N:${document.getElementById("last").value};${document.getElementById("first").value}
TEL:${document.getElementById("vphone").value}
ADR:${document.getElementById("address").value}
END:VCARD`;
      break;

    case "wifi":
      finalData =
`WIFI:T:${document.getElementById("security").value};S:${document.getElementById("ssid").value};P:${document.getElementById("password").value};;`;
      break;
  }

  const formData = new FormData();
  formData.append("url", finalData);

  const res = await fetch("http://127.0.0.1:8000/generate", {
    method: "POST",
    body: formData
  });

  const blob = await res.blob();
  const imgUrl = URL.createObjectURL(blob);

  document.getElementById("qrImage").src = imgUrl;
  document.getElementById("qrImage").style.display = "block";

  const dl = document.getElementById("downloadBtn");
  dl.href = imgUrl;
  dl.style.display = "inline";
}
function goCustom() {
  window.location.href = "custom-qr.html";
}
