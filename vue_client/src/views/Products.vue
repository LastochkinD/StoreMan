<template>
    <div>
      <h1>Список товаров</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Код товара</th>
            <th>Название товара</th>
            <th>Рекомендованная цена</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.product_code }}</td>
            <td>{{ product.product_name }}</td>
            <td>{{ product.rec_price }}</td>
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
        products: []
      };
    },
    mounted() {
      // Запрос к серверу для получения списка товаров
      axios.get('http://127.0.0.1:5000/get_products')
        .then(response => {
          // Установка полученных данных в свойство products
          this.products = response.data;
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
  