import Vue from 'vue';
import Router from 'vue-router';

const routerOptions = [
  { path: '/', component: 'Login', alias: '/login' },
  { path: '/logout', component: 'Logout' },
  { path: '/dashboard', component: 'Dashboard' },
  { path: '/stores', component: 'Stores', props: { store: null } },
  { path: '/stores/:store', component: 'Stores', props: true },
  { path: '/scripts/', component: 'Scripts', props: { script: null } },
  { path: '/scripts/:script', component: 'Scripts', props: true },
];

const routes = routerOptions.map((route) => {
  return {
    ...route,
    component: () => import(`@/views/${route.component}.vue`),
  };
});

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes,
});
