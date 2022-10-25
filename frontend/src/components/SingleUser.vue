<template>
  <div class="h-100 d-flex align-items-center justify-content-center">
    <div class="container w-auto">
      <h1>Пользователь</h1>
      <div v-if="message.text" class="alert" :class="alertClass" role="alert">
        {{ message.text }}
      </div>
      <form @submit.prevent="checkForm">
        <div class="form-group mb-3">
          <label for="name">Имя пользователя</label>
          <input
              type="text"
              class="form-control"
              id="name"
              placeholder="Имя"
              v-model="user.username"
          />
          <small class="form-text text-danger" v-if="'username' in errors">
            {{ errors.username }}
          </small>
        </div>
        <div class="form-group mb-3">
          <label for="password">Пароль</label>
          <input
              type="password"
              class="form-control"
              id="password"
              placeholder="Пароль"
              v-model="user.password"/>
        </div>
        <div class="form-group mb-3">
          <label for="password2">Повторите пароль</label>
          <input
              type="password"
              class="form-control"
              id="password2"
              placeholder="Повторите пароль"
              v-model="user.password2"/>
          <small class="form-text text-danger" v-if="'password' in errors">
            {{ errors.password }}
          </small>
        </div>
        <div class="form-group mb-3">
          <label for="adminType">Роль</label>
          <select
              class="form-select"
              id="adminType"
              v-model="user.admin_type">
            <option value="admin">Администратор</option>
            <option value="super_admin">Господь Бог</option>
          </select>
        </div>
        <button type="button" @click="sendForm" class="btn btn-primary">{{ newUser ? 'Добавить' : 'Сохранить' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "SingleUser",
  data() {
    return {
      newUser: !this.$route.params.id,
      user: {},
      loading: true,
      message: {
        type: "",
        text: "",
      },
      errors: {},
      alertClasses: {
        success: "alert-success",
        error: "alert-danger",
        info: "alert-info",
      },
    };
  },
  computed: {
    alertClass() {
      return this.alertClasses[this.message.type];
    },
  },
  async mounted() {
    try {
      if (this.newUser) {
        this.user.admin_type = "admin";
        return;
      }
      const response = await api.getAdmin(this.$route.params.id);
      this.user = response.data;
    } catch (e) {
      this.message = {
        type: "error",
        text: "Произошла ошибка при загрузке пользователя",
      };
      console.log(e);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async sendForm() {
      this.errors = {};
      if (!this.validateForm())
        return;
      try {
        if (this.newUser) {
          await api.addAdmin(this.user);
          this.message = {
            type: "success",
            text: "Пользователь успешно добавлен",
          };
        } else {
          await api.modifyAdmin(this.user);
          this.message = {
            type: "success",
            text: "Пользователь успешно изменен",
          };
        }
      } catch (e) {
        console.log(e);
        if (e.response && e.response.status === 409) {
          this.message = {
            type: "error",
            text: "Пользователь с таким именем уже существует",
          };
        } else {
          this.message = {
            type: "error",
            text: "Произошла ошибка при сохранении пользователя",
          };
        }
      }
    },
    validateForm() {
      this.errors = {};
      if (!this.user.username) {
        this.errors.username = "Поле обязательно";
      }
      if (this.newUser && !this.user.password) {
        this.errors.password = "Поле обязательно";
      }
      if (this.user.password !== this.user.password2) {
        this.errors.password = "Пароли не совпадают";
      }
      return Object.keys(this.errors).length === 0;
    },
  }
}
</script>

<style scoped>

</style>