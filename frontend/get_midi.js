$(document).ready(() => {
    function run() {
        MIDIjs.play('http://localhost:5000')
    }
    run()
    setInterval(run, 120000)
})