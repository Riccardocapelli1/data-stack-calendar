var data = {
  labels: df3.date,
  datasets: [
    {
      label: 'occurrence',
      data: df3.occurrence,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgba(255, 99, 132, 1)',
    }
  ]
};

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {}
});

// Seleziona tutti i titoli dei paragrafi
const paragraphs = document.querySelectorAll("h2");

// Itera attraverso tutti i titoli dei paragrafi
for (let i = 0; i < paragraphs.length; i++) {
  // Assegna un evento al passaggio del mouse
  paragraphs[i].addEventListener("mouseover", function() {
    // Ingrandisci il titolo del paragrafo
    this.style.fontSize = "30px";
  });

  // Assegna un evento all'uscita del mouse
  paragraphs[i].addEventListener("mouseout", function() {
    // Ripristina le dimensioni originali del titolo del paragrafo
    this.style.fontSize = "25px";
  });
}
