document.getElementById('contactForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  const responseBox = document.getElementById('responseMessage');
  responseBox.textContent = 'Sending...';

  try {
    const response = await fetch('<your-api-url>', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const text = await response.text();
    responseBox.textContent = text;
    responseBox.style.color = 'green';
  } catch (err) {
    responseBox.textContent = 'Failed to send message.';
    responseBox.style.color = 'red';
  }
});
