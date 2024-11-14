function sendRequest() {
    code = document.getElementById('code').value;
    language = document.getElementById('language').value;

    fetch('http://127.0.0.1:8000/compile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: code,
            language: language
        })
    }).then(response => {
        displayOutput("Compiling...");
        displayOutput("Running...");
        if (response.ok) {
            response.json().then(data => {
                displayOutput(data.result);
            }).catch(error => {
                console.error('Error:', error);
            })
            return response.json();
        } else {
            throw new Error('Something went wrong');
        }
    }).catch(error => {
        console.error('Error:', error);
    })
}

function displayOutput(output) {
    document.getElementById('output-text').value = output;
}