  //Timer
  (function () {
    const second = 1000,
          minute = second * 60,
          hour = minute * 60,
          day = hour * 24,
          month = day *30;
  
  
    
    // const countDown = new Date('February 29, 2022 00:01:02').getTime(),
    const countDown = new Date('{{time}}').getTime(),
        x = setInterval(function() {    
  
          const now = new Date().getTime(),
          distance = countDown - now;
  
            document.getElementById("days").innerText = Math.floor(distance / (day)),
            document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
            document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
            document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);
  
          //do something later when date is reached
          // if (distance < 0) {
          //   document.getElementById("headline").innerText = "";
          //   document.getElementById("countdown").style.display = "";
          //   document.getElementById("content").style.display = "";
          //   clearInterval(x);
          //   location.href="{%url 'logout'%}";
          // }
          //seconds
        }, 0)
    }());