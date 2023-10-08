<template>
    <div class="container">
      <h1>Список Клиентов</h1>
      <button class="add-button" @click="showAddClientForm">Добавить Клиента</button>
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
      clients: [],
      isAddClientFormVisible: false,
      newClient: {
        client_name: '',
        client_address: '',
        client_phone: '',
        client_note: ''
      }
    };
  },
  methods: {
    showAddClientForm() {
      this.isAddClientFormVisible = true;
    },
    addClient() {
      // Отправка запроса к серверу для добавления нового клиента
      axios.post('http://127.0.0.1:5000/add_client', this.newClient)
        .then(response => {
          // Обновление списка клиентов после успешного добавления
          this.clients.push(response.data);
          // Скрытие формы добавления клиента
          this.isAddClientFormVisible = false;
          // Очистка полей формы
          this.newClient = {
            client_name: '',
            client_address: '',
            client_phone: '',
            client_note: ''
          };
        })
        .catch(error => {
          console.error('Ошибка при добавлении клиента:', error);
        });
    }
  },
  mounted() {
    // Запрос к серверу для получения списка клиентов
    axios.get('http://127.0.0.1:5000/get_clients')
      .then(response => {
        // Установка полученных данных в свойство clients
        this.clients = response.data;
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });
  }
};
</script>
  
  <style scoped>
/* Определение стилей для кнопки и таблицы */
.container {
  display: flex;
  flex-direction: column;
}

.add-client-form {
  margin-bottom: 20px;
}

.add-button {
  margin-bottom: 10px;
  align-self:flex-start;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
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