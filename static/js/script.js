document.addEventListener('DOMContentLoaded', () => {
  const uploadForm = document.getElementById('uploadForm');
  const reportForm = document.getElementById('reportForm');
  const workerInput = document.getElementById('worker_input');
  const fileInput = document.getElementById('input_form');
  const messageElement = document.getElementById('input_form_message');
  const errorMessage = document.getElementById('error_message');
  const instructionsLink = document.querySelector('a[href="#instructions"]');
  const analyzerLink = document.querySelector('a[href="#analyzer"]');
  const instructionsSection = document.getElementById('instructions');
  const analyzerSection = document.getElementById('analyzer');
  const socket = io.connect();

  socket.on('message', (message) => {
    try {
      console.log(message.data);
      var messagesContainer = document.getElementById('messages');
      messagesContainer.innerHTML = ''; // Clear previous messages
      var messageElement = document.createElement('p');
      messageElement.textContent = message.data;
      messagesContainer.appendChild(messageElement);
    } catch (error) {
      console.log(error); // Log any errors to the console
    }
  });
  
  instructionsSection.style.display = 'none';
  analyzerSection.style.display = 'block';

  fileInput.addEventListener('change', (event) => {
    errorMessage.style.display = 'none';
    reportForm.style.display = 'none';
      const files = event.target.files;
      if (files.length > 0) {
          const fileNames = Array.from(files).map(file => file.name);
          messageElement.textContent = `Files successfully uploaded: ${fileNames.join(', ')}`;
      }
  });

  uploadForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = new FormData(uploadForm);
      fetch('/upload', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          if ('error' in data) {
            const errorMessage = document.getElementById('error_message');
            errorMessage.textContent = data.error;
            errorMessage.style.display = 'block'; }
          else {
            data.forEach(worker => {
                const option = document.createElement('option');
                option.value = worker;
                option.textContent = worker;
                workerInput.appendChild(option);
          });
          reportForm.style.display = 'block';
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });

  function showSection(sectionId) {
    instructionsSection.style.display = 'none';
    analyzerSection.style.display = 'none';

    const sectionToShow = document.getElementById(sectionId);
    sectionToShow.style.display = 'block';
}

function handleNavLinkClick(event) {
  event.preventDefault();
  const sectionId = this.getAttribute('href').substring(1);
  showSection(sectionId);
}

  instructionsLink.addEventListener('click', handleNavLinkClick);
  analyzerLink.addEventListener('click', handleNavLinkClick);

});
