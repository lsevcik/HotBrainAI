next();
function next(){
  const arrowR = document.getElementById("next")
  const image = document.getElementById("slide")
  const text = document.getElementById("slidetext")
  var counter=1;


  arrowR.onclick = function(){
  if(counter==0)
    {
      image.src="/static/images/brainbit.jpg";
      text.textContent = "A comfortable device that fits around your head and reads your reactions to imagery. Delivering the info to our database."
      counter++;
    }
  else if(counter==1)
    {
      image.src="/static/images/computerbrain.jpg";
      text.textContent = "After taking your scan, we process your brainwaves alongside other members and through our calculations we can match you with like-minded folk."
      counter++;
    }
  else if(counter==2)
    {
      image.src="/static/images/couple.avif";
      text.textContent = "The end result. You. Them. Happy together!"
      counter=0;
    }
  }
};

prev();
function prev(){
  const arrowL = document.getElementById("prev")
  const image = document.getElementById("slide")
  const text = document.getElementById("slidetext")
  var counter=1;


  arrowL.onclick = function(){
  if(counter==0)
    {
      image.src="/static/images/couple.avif";
      text.textContent = "The end result. You. Them. Happy together!"
      counter=2;
    }
  else if(counter==1)
    {
      image.src="/static/images/brainbit.jpg";
      text.textContent = "A comfortable device that fits around your head and reads your reactions to imagery. Delivering the info to our database."
      counter--;
    }
  else if(counter==2)
    {
      image.src="/static/images/computerbrain.jpg";
      text.textContent = "After taking your scan, we process your brainwaves alongside other members and through our calculations we can match you with like-minded folk."
      counter--;
    }
  }
};
