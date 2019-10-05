FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY development.conf /etc/nginx/conf.d/development.conf

CMD ["nginx", "-g", "daemon off;"]