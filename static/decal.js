export function setBackground() {
    const images = [
        'beachSunset.png',
        'sunset.png',
        'pourPaint.png',
        'abstract.png',
        'space.png'
    ]
    let selectedBackground = `./static/images/${images[Math.floor(Math.random()*images.length)]}`
    console.log(selectedBackground)
    document.getElementById("backdrop").style.backgroundImage = `url(${selectedBackground})`;
}