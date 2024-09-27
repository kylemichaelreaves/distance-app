// src/main.ts

import {createApp} from 'vue';
import './style.css';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // Import the Element Plus CSS


const app = createApp(App);
app.use(ElementPlus);
app.mount('#app');

