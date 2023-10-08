<template>
    <div class="modal">
      <div class="modal-content">
        <h2>Добавить клиента</h2>
        <form @submit.prevent="addClient">
          <!-- Форма для добавления клиента -->
          <!-- ... (поля для ввода информации о клиенте) ... -->
  
          <button type="submit">Добавить</button>
          <button type="button" @click="closeModal">Отмена</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      addClient() {
        // Логика добавления клиента (вы можете использовать this.$emit('add-client', this.newClient);)
        // Закрыть модальное окно
        this.closeModal();
      },
      closeModal() {
        // Закрыть модальное окно
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    /* Стили для модального окна (например, фон, позиция и т.д.) */
  }
  
  .modal-content {
    /* Стили для содержимого модального окна (например, ширина, высота, отступы и т.д.) */
  }
  </style>
  