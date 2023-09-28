UPDATE web_piloto
SET imagen = '/media/perfil-de-usuario.webp'
WHERE imagen = '/static/media/perfil-de-usuario.webp';


UPDATE web_equipo
SET imagen = '/media/Imagen_no_disponible.png'
WHERE imagen = '/static/media/Imagen_no_disponible.png';

UPDATE web_temporada
SET imagenHistorica = "//upload.wikimedia.org/wikipedia/commons/9/9c/Fernando_Alonso_2006_Malaysia.jpg"
WHERE anyo = 2006;

UPDATE web_temporada
SET imagenHistorica = "//upload.wikimedia.org/wikipedia/commons/thumb/7/71/Schumacher_china_2012.jpg/320px-Schumacher_china_2012.jpg"
WHERE anyo IN (2000, 2001, 2002);
