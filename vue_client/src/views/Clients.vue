<template>
    <div>
      <h1>Список Клиентов</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Клиент</th>
            <th>Адрес</th>
            <th>Телефон</th>
            <th>Примечание</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="client in clients" :key="client.id">
            <td>{{ client.id }}</td>
            <td>{{ client.client_name }}</td>
            <td>{{ client.client_address }}</td>
            <td>{{ client.client_phone }}</td>
            <td>{{ client.client_note }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        clients: []
      };
    },
    mounted() {
      // Запрос к серверу для получения списка товаров
      axios.get('http://127.0.0.1:5000/get_clients')
        .then(response => {
          // Установка полученных данных в свойство products
          this.clients = response.data;
        })
        .catch(error => {
          console.error('Ошибка при получении данных:', error);
        });
    }
  };
  </script>
  
  <style scoped>
  /* Стили для таблицы могут быть добавлены здесь */
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
  }
  </style>
  