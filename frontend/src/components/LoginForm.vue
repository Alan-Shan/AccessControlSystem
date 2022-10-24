<template>
  <main class="form-signin">
    <form @keydown.enter="login">
      <h1 class="h3 mb-3 fw-normal">Авторизация</h1>
      <div class="alert alert-danger" v-if="error.length" role="alert">
        {{ error }}
      </div>
      <div class="form-floating">
        <input type="text" class="form-control" v-model="this.p" id="usernameInput" placeholder="user">
        <label for="usernameInput">Имя пользователя</label>
      </div>
      <div class="form-floating">
        <input type="password" class="form-control" id="passwordInput" placeholder="****">
        <label for="passwordInput">Пароль</label>
      </div>

      <div class="checkbox mb-3">
        <label>
          <input type="checkbox" value="remember-me"> Запомнить меня
        </label>
      </div>
      <button class="w-100 btn btn-lg btn-primary" @click="login" type="button">Вход</button>
    </form>
  </main>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    login() {
      this.$store.dispatch("auth/login", {
        email: this.email,
        password: this.password,
      }).then(() => {
        this.$router.push({ name: "Home" });
      }).catch((error) => {
        // check for null error
        if (error.response) {
          this.error = error.response.data.message;
        } else {
          this.error = "Неизвестная ошибка";
        }
      });
    },
  },
}
</script>

<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .checkbox {
  font-weight: 400;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

</style>