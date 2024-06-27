import {service} from "./js/datebaseConfig.js"

const endPoint = "/Ingrid"

// Definindo estrutura do corpo do meu objeto do banco.
var body = {
    
}

// Carregando dados do meu banco
const loadData = () => {
    service.load(endPoint).then( data => {
        body = data;
        console.log(body);

        getLightsValues()
        getTvValues()
        setTempValues()
    })
}

// Definindo os dados no meu banco.
// service.set(endPoint, body)

// ==================  Colocando os dados no HTML   ==================
const getLightsValues = (idLocal = 'LivingRoom') => {
    let lamp = document.getElementById('lightBulb' + idLocal)
    let lightOn = false;

    //body.Led pega o valor de 'Led' do banco de dados
    lightOn = body.Led;

    if(lightOn){ 
        lamp.classList.add("light-on")
    } else {
        lamp.classList.remove("light-on")
    }
}

const getTvValues = (idLocal = 'LivingRoom') => {
    let tv = document.getElementById(idLocal + "Tv")
    let tvOn = false;

    tvOn = body.Tv;

    if(tvOn){ 
        tv.innerHTML = 'ON'
    } else {
        tv.innerHTML = 'OFF'
    }
}

const setTempValues = (idLocal = 'LivingRoom') => {
    const TempElement = document.getElementById(idLocal + "Temp")
    const HumidElement = document.getElementById(idLocal + "Humidity")

    let Hvalue = 0;
    let Tvalue = 0;

    Hvalue = body.Umidade;
    Tvalue = body.Temperatura;
    
    TempElement.innerHTML = Tvalue + " °C "
    HumidElement.innerHTML = Hvalue + " % "
}

// ================== Funções de Interação com HTML ==================

const toggleLamp = (idRoom = 'LivingRoom') => {
    const element = document.getElementById("lightBulb" + idRoom);
    element.classList.toggle('light-on');

    body.Led = !body.Led;
    service.set(endPoint, body);

}

const toggleTv = (idRoom = 'LivingRoom') => {
    const element = document.getElementById(idRoom + "Tv")
    let isOn = false;

    body.Tv = !body.Tv;
    isOn = body.Tv;
    service.set(endPoint, body);

    if(isOn) {
        element.innerHTML = "ON"
    } else {
        element.innerHTML = "OFF"
    }
}

console.log('script loaded');

//! Adicionando as funções no HTML 

window.toggleLamp = toggleLamp
window.toggleTv = toggleTv

setInterval(() => {
    loadData();
}, 2000);