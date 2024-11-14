function sendRequest() {
    code = document.getElementById('code').value;
    language = document.getElementById('language').value;

    console.log("Sending request...");
    console.log("Code: " + code);
    console.log("Language: " + language);
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
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Something went wrong');
        }
    }).catch(error => {
        console.error('Error:', error);
    })
}