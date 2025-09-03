usar flask, PyJWT


1. Crear la carpeta de claves

Dentro del proyecto, crea la carpeta donde se guardarán las claves:

mkdir -p auth/keys

2. Generar la clave privada
openssl genpkey -algorithm RSA -out auth/keys/private.pem -pkeyopt rsa_keygen_bits:2048

3. Generar la clave pública
openssl rsa -pubout -in auth/keys/private.pem -out auth/keys/public.pem

4. Notas importantes

No subir la clave privada al repositorio. Solo la pública puede compartirse si es necesario.

Cada desarrollador que clone el proyecto debe generar su propio par de claves siguiendo estos pasos.