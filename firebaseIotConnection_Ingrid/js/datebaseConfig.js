
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js';
import { getDatabase, ref, set, onValue } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-database.js';

const firebaseConfig = {
    apiKey: "",
    authDomain: "",
    databaseURL: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

const service = {}

service.load =  (username) => {
    console.log("loading data...");
    const userref = ref(database, username)
    
    return new Promise((resolve, reject) => {
        onValue(userref, (snapshot) => {
            const data = snapshot.val();
            if(data) {
                resolve(data);
            } else {
                reject(new Error("No data avaliable!"))
            }
        }, (error) => {
            reject(error)
        })
    }) 
}

service.set = (url, data) => {
    set(ref(database, url ), data)
}


export {service}