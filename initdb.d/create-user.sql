CREATE USER `sample`@`localhost` IDENTIFIED BY 'sample';
GRANT ALL PRIVILEGES ON django_sample.* TO `sample`@`localhost`;
FLUSH PRIVILEGES;

