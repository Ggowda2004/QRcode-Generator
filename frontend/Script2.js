// ------------------ GLOBAL ------------------
const qrTextInput = document.getElementById("qrText");
const bodyColorInput = document.getElementById("bodyColor");
const cornerColorInput = document.getElementById("cornerColor");
const cornerTypeSelect = document.getElementById("cornerType");
const logoInput = document.getElementById("logoInput");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const downloadBtn = document.getElementById("downloadBtn");

const BASE_URL = "https://qrcode-generator-18jm.onrender.com/api/v1/qr/custom-qr";

// ------------------ GENERATE ------------------
async function generate() {
  const data = qrTextInput.value.trim();
  if (!data) return alert("Please enter text or URL for QR code.");

  const formData = new FormData();
  formData.append("data", data);
  formData.append("qr_fill", parseColor(bodyColorInput.value));
  formData.append("box_color", parseColor(cornerColorInput.value));
  formData.append("box_position", cornerTypeSelect.value);

  if (logoInput.files[0]) {
    formData.append("center_logo", logoInput.files[0]);
  }

  try {
    const res = await fetch(BASE_URL, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      console.error("Backend error:", err);
      return alert(JSON.stringify(err, null, 2));
    }

    const blob = await res.blob();
    displayQR(blob);

  } catch (err) {
    console.error(err);
    alert("Something went wrong while generating the QR code.");
  }
}

// ------------------ DISPLAY (HIGH DPI) ------------------
function displayQR(blob) {
  const imgUrl = URL.createObjectURL(blob);

  const qrImage = new Image();
  qrImage.onload = () => {
    const dpr = window.devicePixelRatio || 1;

    // Set canvas for high-DPI
    canvas.width = 320 * dpr;
    canvas.height = 320 * dpr;
    canvas.style.width = "320px";
    canvas.style.height = "320px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // scale context
    ctx.clearRect(0, 0, 320, 320);

    ctx.drawImage(qrImage, 0, 0, 320, 320);

    URL.revokeObjectURL(imgUrl);

    // Show download button
    downloadBtn.style.display = "inline-block";
  };
  qrImage.src = imgUrl;
}

// ------------------ DOWNLOAD ------------------
function downloadQR() {
  const data = canvas.toDataURL("image/png"); // get high-DPI image from canvas
  const a = document.createElement("a");
  a.href = data;
  a.download = "custom_qr.png";
  a.click();
}

// ------------------ HELPERS ------------------
function parseColor(hex) {
  const r = parseInt(hex.substr(1, 2), 16);
  const g = parseInt(hex.substr(3, 2), 16);
  const b = parseInt(hex.substr(5, 2), 16);
  return `${r},${g},${b}`;
}

// ------------------ BACK BUTTON ------------------
function goBack() {
  window.location.href = "index.html";
}

// ------------------ EVENT BINDINGS ------------------
downloadBtn.style.display = "none";
