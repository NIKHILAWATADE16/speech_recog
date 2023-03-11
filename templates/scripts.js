function voice() {
    // var recognition = new webkitSpeechRecognition();
    // recognition.lang = "en-GB";
    // recognition.onresult = function (event) {
    //     // console.log(event);
    //     document.getElementById("message").value = event.results[0][0].transcript;

    // }
    // recognition.start();
    var speech = true;
    window.SpeechRecognition = window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();
    recognition.interimResults = true;

    recognition.addEventListener('result', e => {
        const transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('')

        document.getElementById("message").innerHTML = transcript;
        console.log(transcript);
    });
    
    if (speech == true) {
        recognition.start();
    }

}


// click_to_record.addEventListener('click',function(){
//     var speech = true;
//     window.SpeechRecognition = window.webkitSpeechRecognition;

//     const recognition = new SpeechRecognition();
//     recognition.interimResults = true;

//     recognition.addEventListener('result', e => {
//         const transcript = Array.from(e.results)
//             .map(result => result[0])
//             .map(result => result.transcript)
//             .join('')

//         document.getElementById("message").innerHTML = transcript;
//         console.log(transcript);
//     });
    
//     if (speech == true) {
//         recognition.start();
//     }
// })