<template>
  <div class="container">
    <h1>Список Клиентов</h1>
    <button class="add-button" @click="showAddClientForm(-1)">Добавить Клиента</button>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Клиент</th>
          <th>Адрес</th>
          <th>Телефон</th>
          <th>Примечание</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="client in clients" :key="client.id">
          <td>{{ client.id }}</td>
          <td>{{ client.client_name }}</td>
          <td>{{ client.client_address }}</td>
          <td>{{ client.client_phone }}</td>
          <td>{{ client.client_note }}</td>
          <td>
            <button @click="showAddClientForm(client.id)">Открыть</button>
            <button @click="showDelClientForm(client.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно для удаления клиента-->
    <div v-if="isDelClientFormVisible" class="modal">
        <!-- Содержимое модального окна -->
        <div class="modal-content">
            <span class="close">&times;</span>
            <p>Вы уверены, что хотите удалить запись?</p>
            <button @click=closeDelModal>Отмена</button>
            <button @click=delClient(this.deleting_client)>Подтвердить удаление</button>
        </div>
    </div>

    <!-- Модальное окно для добавления клиента -->
    <div v-if="isAddClientFormVisible" class="modal">
      <div class="modal-content">
        <h2>Добавить клиента</h2>
        <form @submit.prevent="addClient">
        <div class="form-container">
                <div class="form-group">
                    <div class="nameform">
                        <label for="client_name">Имя клиента:</label>
                    </div>
                    <div class="inputform">
                        <input type="text" id="client_name" v-model="newClient.client_name" required>
                    </div>
                </div>
                <div class="form-group">
                    <div class="nameform">
                        <label for="client_address">Адрес:</label>
                    </div>
                    <div class="inputform">
                        <input type="text" id="client_address" v-model="newClient.client_address" required>
                    </div>
                </div>
                <div class="form-group">
                    <div class="nameform">
                        <label for="client_phone">Телефон:</label>
                    </div>
                    <div class="inputform">
                        <input type="tel" id="client_phone" v-model="newClient.client_phone" required>
                    </div>             
                </div>
                <div class="form-group">
                    <div class="nameform">
                        <label for="client_note">Примечание:</label>
                    </div>
                
                  <div class="inputform">
                    <textarea id="client_note" v-model="newClient.client_note"></textarea>
                  </div>
                </div>
                <div class="button-container">
                  <button type="submit">Добавить</button>
                  <button type="button" @click="closeModal">Отмена</button>
                </div>
        </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      clients: [],
      isAddClientFormVisible: false,
      isDelClientFormVisible: false,
      clientFormMode: 0,
      deleting_client: -1,
      newClient: {
        client_name: '',
        client_address: '',
        client_phone: '',
        client_note: ''
      }
    };
  },
  methods: {
    showAddClientForm(client_id) {
      if (client_id!=-1){
        this.clientFormMode = 1;
        this.newClient = this.clients[this.clients.findIndex(client => client.id === client_id)];
      }
      else {
        this.clientFormMode = 0;
        this.newClient = {
              client_name: '',
              client_address: '',
              client_phone: '',
              client_note: ''
            };
      }
      this.isAddClientFormVisible = true;
    },
    showDelClientForm(client_id) {
      this.deleting_client = client_id
      this.isDelClientFormVisible = true;
    },
    addClient() {
      if (this.clientFormMode ==0){
        // Отправка запроса к серверу для добавления нового клиента
        axios.post('http://127.0.0.1:5000/add_client', this.newClient)
          .then(response => {
            // Обновление списка клиентов после успешного добавления
            this.clients.push(response.data);
            // Скрытие формы добавления клиента
            this.closeModal();
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
      else {
        // Отправка запроса к серверу для добавления нового клиента
        axios.post('http://127.0.0.1:5000/update_client', this.newClient)
          .then(response => {
            // Обновление списка клиентов после успешного добавления
            // Скрытие формы добавления клиента
            this.closeModal();
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
    delClient(client_id){
      // Отправка запроса к серверу для удаления клиента
      axios.post('http://127.0.0.1:5000/del_client', {'client_id':client_id})
        .then(response => {
          // Обновление списка клиентов после успешного добавления
          const index = this.clients.findIndex(client => client.id === client_id);
          // Если клиент с указанным id найден, удаляем его из массива
          if (index !== -1) {
          this.clients.splice(index, 1);
          } else {
            console.error('Клиент с указанным id не найден.');
          }
          // Скрытие формы добавления клиента
          this.closeDelModal();
          this.deleting_client = -1;
          // Очистка полей формы
        })
        .catch(error => {
          console.error('Ошибка при добавлении клиента:', error);
        });
    },
    closeModal() {
      // Закрыть модальное окно
      this.isAddClientFormVisible = false;
    },
    closeDelModal() {
      // Закрыть модальное окно
      this.isDelClientFormVisible = false;
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
  align-self: flex-start;
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

/* Стили для модального окна и его содержимого */
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.button-container {
  margin-top: 20px;
  text-align: right;
}

.form-container {
    display: flex;
    max-width: 400px;
    flex-flow: column wrap;
}
.form-group {
    width: 100%;
    display: flex;
    padding-top: 1em;
}
.inputform {
    text-align: right;
    width: 50%;
}
.nameform {
    width: 50%;
}
.button-container {
    padding-top: 1em;
    text-align: right;
}

/* Стили для кнопок */
button {
  padding: 10px 20px;
  margin-left: 10px;
  border: none;
  background-color: #007bff;
  color: #ffffff;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
