# qty_fin
python flask blueprint 


# boot in ide
```shell
run ./qty_fin.py
```

then visit http://localhost:9999


# publish in docker
Dockerfile and your code

![image](https://note.youdao.com/yws/public/resource/635a3b759d31135cbd682b30242bbf8b/xmlnote/FC059B7230644C3FBDE606EAA02841C2/26941)

put code in the folder 'app'

![image](https://note.youdao.com/yws/public/resource/635a3b759d31135cbd682b30242bbf8b/xmlnote/07528F265A584D2A9872F966FEF28068/26943)

docker build

```shell
docker build -t qtyfin_i .
```

run docker container
```shell
docker run --net=host --name qtyfin_c -itd qtyfin_i
```

# install nginx 
visit [How to install nginx](https://github.com/chenzhaoplus/linux-scripts/tree/master/nginx)

# add nginx server config
```
server {
    listen       8888;
    server_name  localhost;
    
    # front server proxy
    location / {
        try_files $uri  /index.html;
        root   /usr/local/nginx/front/qtyfin/dist;
        index index.html; 
    }
    # backend server proxy
    location ^~/backend {
        proxy_pass http://localhost:9999/;   # the last '/' is necessary
        proxy_redirect off;
        #proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;             
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;             
        proxy_set_header Host $http_host;         
        client_max_body_size 10m;
        proxy_connect_timeout 90;
        proxy_read_timeout 90;  
        proxy_set_header Cookie $http_cookie;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
    
    location ~ /.ht {
        deny  all;
    }
}
```

