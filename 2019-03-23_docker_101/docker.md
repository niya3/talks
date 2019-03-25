# Docker 101
От Dockerfile к контейнеру через докер-образ

# whoami

Знаком с docker ~год.

* отвечаю за сборку, тестирование и публикацию образов приложений
* добавляю полученные образы в оркестратор Kubernetes
* локально разрабатываю приложения как в контейнере, так и с использованием контейнеров

* работал через контейнеры с LaTeX и Jupyter Notebook, чтобы зависимости не разбежались по системе.

# docker

Презентация актуальна для последней версии на сегодня(25.03.2019) версии docker:

```
$ docker version | grep Ver
Version:          18.09.3-ce
Version:          18.09.3-ce
```

Docker - ПО(написанное на Go), отвечающее за упаковку и распространение приложений в полном окружении(зависимости, переменные, настройки), изолированный запуск приложений(контейнеров) и взаимодействия контейнеров.

Преимущества docker:
1. Можно написать для своей программы описание, которое позволяет упаковать программу её вместе с зависимостями, и они не будут конфликтовать с зависимостями других приложений.
1. Это приложение можно запустить на любой ОС, в которой есть Docker - Linux, Windows, MacOS, не зависимо от того, какой дистрибутив Linux был взят за основу твоего образа.
1. Больше ты не программист локалхоста. "На моей машине всё работает" больше не работает - держи Dockerfile, который демонстрирует ошибку.
1. Можно так же поднимать вспомогательные сервисы, чистые или уже преднастроенные.

Docker не изобрёл контейнеры, но популяризовал их.

![](https://docs.docker.com/engine/images/engine-components-flow.png)


[Docker overview](https://docs.docker.com/engine/docker-overview/)

```
docker ==
namespaces +
cgroups +
capabilities +
UnionFS
```

1. [Механизмы ядра](https://itnext.io/chroot-cgroups-and-namespaces-an-overview-37124d995e3d) дают изоляцию, ограничения ресурсов и возможностей, что позволяет создать для контейнера "песочницу" и иллюзию единственности. Работаем напрямую с ядром ОС, практически без накладных расходов, ведь эти механизмы и так используются при запуске обычного процесса.

1. Файловые системы вроде UnionFS эффективно работают со слоями, экономя дисковое пространство и сетевой трафик.

## [Основные понятия](https://vsupalov.com/6-docker-basics/)

| Dockerfile | Образ | Контейнер |
|---|---|---|
| Набор инструкций | Результирующая корневая* система | Процесс запущенный в своём окружении поверх корневой системы|
| Чертёж формы для отливки | Форма для отливки | Отлитые из формы детали |

\* - дополнена мета-информацией, не все команды генерируют файлы(смена рабочей директории, пользователя и т.п.)

![](https://docs.docker.com/engine/images/architecture.svg)

Клиент может быть на одной машине, а демон на другой. С демоном можно работать через API.

### Dockerfile

Dockerfile - текстовый файл, в котором указан набор инструкций с ключевыми словами.

* Каждая инструкция из Dockerfile выполняется в отдельном шаге сборки
* Каждый шаг сборки генерирует один слой.
  * Слой содержит файлы(или мета-информацию), которые изменились после выполнения текущей инструкции
  * Если инструкция завершилась с ошибкой, то слой не создаётся
  * Если все слои создались успешно, то последний из них помечается заданным именем образа

![](https://fabianlee.org/wp-content/uploads/2017/05/dockviz-images-whalesay.png)

Dockerfile неотделим от кода и хранится в репозитории с кодом, он описывает "как готовить" ваше приложение.

### Образ

Аналогия с историей git: слой - ревизия, слои образуют дерево. В корне дерева специальный пустой образ `scratch`. Образ - состояние рабочей директории для некоторой ревизии.

![](https://docker-doc.readthedocs.io/zh_CN/latest/_images/docker_images.gif)

Образ - слепок корневой файловой системы, который "склеивается" из нескольких слоёв(начиная от `scratch` до слоя, помеченного именем образа). Слои read-only, разделяемые(Copy-on-Write).
- образы, у которых есть общие слои, занимают в сумме меньше места
- несколько контейнеров из одного образа займут лишь чуть больше места, чем один контейнер
- по сети передаются только недостающие слои, не все

![](https://www.shellhacks.com/wp-content/uploads/container-layers.jpg.pagespeed.ce.r3DaV3pkFI.jpg)

### Контейнер 

Контейнер - просто запущенный процесс(в контейнере имеет PID=1), со своей корневой системой и переменными окружения. Контейнер жив, пока жив породивший его процесс.

При создании контейнера поверх слоёв образа(доступны только на чтение) создаётся слой контейнера(доступный на запись). У каждого контейнера этот слой свой. Слой уничтожается при удалении контейнера. Решение - храните данные вне контейнера, пробрасывайте директории (mount/volume) или передавайте по сети.

![](https://www.shellhacks.com/wp-content/uploads/sharing-layers-700x422.jpg.pagespeed.ce.EtlLclpCLn.jpg)

Контейнер - не виртуальная машина, ядро ОС используется напрямую, без гипервизора.


![](http://imesh.github.io/images/contvsvm.png)


Скачаем образ, создадим, запустим и подключимся к контейнеру (в одно действие), чтобы убедиться что на нашей системе всё работает правильно.
```
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:2557e3c07ed1e38f26e389462d03ed943586f744621577a99efb77324b0fe535
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
...
```

[Образ vs Контейнер](https://www.shellhacks.com/ru/docker-image-vs-container/)


# Сборка

Простой Dockerfile: в образе на основе минималистичного дистрибутива Alpine Linux создадим файл и укажем, что вновь созданный контейнер при запуске должен вывести содержимое этого файла на экран.

```
$ cat Dockerfile
FROM alpine
RUN echo "Hello world!" > /tmp/greeting
WORKDIR /tmp
CMD cat ./greeting
```
Собираем, просим пометить образ тэгом tmp_hi:latest, и передать в контекст сборки содержимое текущей директории: `.`

```
$ docker build --tag tmp_hi .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM alpine
 ---> 5cb3aa00f899
Step 2/4 : RUN echo "Hello world!" > /tmp/greeting
 ---> e0a0ac849e2d
Step 3/4 : WORKDIR /tmp
 ---> c35889c8514c
Step 4/4 : CMD cat ./greeting
 ---> 1bdcfd5a4d3d
Successfully built 1bdcfd5a4d3d
Successfully tagged tmp_hi:latest
```
Проверяем что образ появился, создаём и запускаем контейнер.

```
$ docker images | grep hi
tmp_hi              latest              1bdcfd5a4d3d        2 minutes ago       5.53MB

$ docker run tmp_hi
Hello world!
```

## Контекст сборки

Контекст сборки - содержимое каталога, указанного последним параметром команды `build`, за исключением файлов, подходящих под шаблоны в `.dockerignore`. Из контекста сборки нужно исключить все файлы, которые не нужны для сборки/работы вашего приложения. Прямая аналогия с `.gitignore`.

Следующие инструкции закончатся с ошибкой, т.к. пытаются обратиться к файлам, которых нет в контексте:

```
COPY no_such_file .

COPY /tmp/tmp .

COPY ../../level_up .
```

## Пример Dockerfile

В `Dockerfile` нет ветвлений, циклов, но есть "наследование" и отложенное выполнение инструкций помеченных ключевым словом `ONBUILD`(очень редко используется). Всего чуть больше 20 инструкций.

****

`#` строка **начинающая** с символа решётки - комментарий.

`\ ` экранирует перевод строки

****

Пример Dockerfile, компилирующий приложение написанное на ЯП Go.

```
FROM golang:1.11.6-alpine3.8 as build_image
WORKDIR /go/src/company.com/product_name/

# install deps

RUN apk add --no-cache git protobuf protobuf-dev
RUN go get -u \
        github.com/golang/protobuf/protoc-gen-go \
        github.com/sirupsen/logrus

# generate proto

COPY api/. api/
COPY pkg/proto/ pkg/proto
RUN protoc \
        -I /usr/include -I api/ \
        api/product.proto \
        --plugin=$GOPATH/bin/protoc-gen-go \
        --go_out=pkg/product_proto

# build

COPY . .
RUN go build ./cmd/exe

# Multi-stage! Copy artifact
FROM alpine:3.8 as release_image
WORKDIR /artifact
COPY --from=build_image /go/src/company.com/product/exe exe
CMD exe

# meta-info

EXPOSE 1234
ARG BUILD_DATE="1970-01-01T00:00:00Z"
ARG VCS_BRANCH="unkhown"
ARG VCS_REF="unkhown"
LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-branch=$VCS_BRANCH \
      org.label-schema.vcs-ref=$VCS_REF
```

Получившийся в итоге образ не содержит зависимостей, файлов компилятора и даже исходных файлов нашего приложения. Итоговый образ занимает всего 5МБ + размер приложения, а один только родительский образ первого образа занимает 100МБ+.

[Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

## Оптимизируем размер образа

1. Сливаем `RUN` инструкции в одну, в конце **этой же инструкции** удаляем ненужные файлы, чтобы не плодить слои, т.к. это остаётся в истории
1. Используем готовые родительские образы - `continuumio/anaconda3` вместо установки `python + anaconda` на `debian`
1. Mutli-stage: в новый релизный образ копируется только артефакт, а сборочные зависимости, приватные файлы, токены, ключи и т.п. остаётся в сборочном образе, который не покидает пределов сборочной машины.
1. Переносим [специальным образом скомпилированный](https://medium.com/@chemidy/create-the-smallest-and-secured-golang-docker-image-based-on-scratch-4752223b7324) артефакт в пустую корневую систему: [`FROM scratch`](https://hub.docker.com/_/scratch) 

[Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## Оптимизируем время сборки

Правильное использование кэша существенно ускоряет **повторную** сборку образа: `Using cache` :heart:

Слой переиспользуется, если:
* предыдущий слой был взят из кэша и если не изменились:
  * сама строка с инструкцией
  * чек-суммы файлов, копируемых из контекста на **данном шаге** `COPY one_file .` vs `COPY . .`
  * переданные значения `ARG`

Следим за кэшем:

1. Указываем в [`.dockerignore`](https://docs.docker.com/engine/reference/builder/#dockerignore-file) всё, что не относится к сборке приложения, синтаксис регулярных выражения Go
```
.git
.*
!.clang-format
Dockerfile
README.md
```
2. Порядок директив: сначала делать то, что реже меняется и сильно влияет на остальные слои
    * сначала установи компилятор, потом скопируй своё приложение
3. Порядок копирования файлов:

```
COPY my_app ./my_app                        |   COPY my_app/requirments.txt /tmp/req.txt
RUN cd my_app && python setup.py install    |   RUN pip install -r /tmp.req.txt
                                            |   COPY my_app ./my_app
                                            |   RUN cd my_app && python setup.py install
```

***

* Сборка с явным указанием образов, с которых надо взять кэш: `docker build --cache-from=name1 --cache-from=name2`, **но**
    * слои прочих доступных образов не анализируется и кэш не используются
    * указанные образы **уже** должны быть загружены на машину
* **NB** Для эффективной пересборки mutli-stage необходимо иметь кэш всех образов, а не только последнего
* Сборка всего образа с нуля: `docker build --no-cache`
* [Как разрушить кэш, начиная с некоторого шага](https://github.com/moby/moby/pull/10682):

```
...
# нижеследующие инструкции всегда будут выполняться заново
ARG EPOCH 0
# следующий файл часто обновляется и каждую пересборку нам важно получать актуальную версию
RUN wget http://can.be/updated/at/any/time
...

$ docker build --build-arg TIMESTAMP=$(date +%s) ...
```


[Leverage build cache](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache)


# Командная строка

## Работа с образами

`images` - список образов на нашей машине

`build` - создать новый образ из локального Dockerfile или удалённого. **NB**  `git://` только для [ssh по 22 порту](https://github.com/moby/moby/pull/33711#issuecomment-373807568)

`history` - смотрим, как образ был получен. **NB** все инструкции, файлы, переменные окружения остаются в истории образа! Используйте `squash`(склеить все слои в один) или `muiti-stage`, чтобы замести следы.

`rmi` - удаляем образ

`tag` - добавляем ему ярлыки для версионирования: имя-порт реестра в которое будем выгружать, имя образа, тэг

```
myregistryhost:5000/fedora/httpd:version1.0
[   [host]    [:port]/]name     [:tag]
```

`search` найти образ в реестре(реестр по умолчанию: [Docker Hub](https://hub.docker.com/))

`pull` загрузить с реестра

`push` выгрузить в реестр

`login/logout` "войти"/"выйти". **NB** аутентификационные данные хранятся в base64 `~/.docker/config.json`

`save/load` запаковать/распаковать образ как tar-архив с мета-информацией, может пригодиться для переноса на удалённую машину в обход реестра.

**NB** с каким тэгом запакуешь, с таким и распакуешь

**NB** `save image1:x image2:y image3:z` создаст один архив меньшего размера, чем три команды (если есть общая история)

## Работа с контейнерами

`run = [pull] + create + start + attach` - [скачает образ], создаст контейнер, запустит и подключится к его stdin/stderr

`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

* `--rm` удалить контейнер по завершении процесса
* `-ti` запустить в интерактивном режиме, подключиться к stdin
* `-p 8080:80` пробросить порт с хостовой машины в порт контейнера
* `-v /abs/host/path:/container/path` смонтировать директорию с хостовой машины в контейнер
* `-v volume_name:/container/path` смонтировать [volume](https://docs.docker.com/storage/volumes/)
* `--sysctl` задать [параметры ядра](https://docs.docker.com/v17.09/engine/reference/commandline/run/#configure-namespaced-kernel-parameters-sysctls-at-runtime)
* ...

```
# ключей очень много
docker run --help | wc -l
97
```

***

`exec` запустит новый процесс в контексте запущенного контейнера

`logs` - просмотр логов контейнера. **NB**: хорошая практика для приложений - писать в stderr/stdout

`ps` - выведет список активных контейнеров; `ps -a` всех, включая завершившиеся

```
# что бывает, когда делаешь run без --rm
$ docker ps | wc -l
1
$ docker ps -a | wc -l
100500
```

`rm -f` - удалит контейнер (-f остановит при необходимости)

`inspect` - вывести информацию об объектах docker: образ, контейнер, сеть, ...

`commit` - создаст **образ из контейнера**

`export/import` - запакует/распакует как tar-архив

## Чистка, уход за системой

```
docker container prune
docker image prune
docker volume prune
docker network prune
```

```
$ docker system prune -a --volumes

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all volumes not used by at least one container
        - all images without at least one container associated to them
        - all build cache
```

```
$ docker system df
TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              26                  22                  186.8MB             77.49MB (41%)
Containers          33                  0                   16.33MB             16.33MB (100%)
Local Volumes       0                   0                   0B                  0B
Build Cache         0                   0                   0B                  0B
```

# Типичные проблемы из [@docker_ru](https://t.me/docker_ru)

## Ошибки пользователя

1. Помни про контекст ->
1. Проверь `.dockerignore`
    - `Dockerifle` должен быть в контексте
1. Различай время сборки и время выполнения
    - монтирование: `volume` и `mount` возможно только в run-time
    - ARG задаётся и доступна в сборке
    - ENV параметризуется при выполнении


## Windows

1. Docker for Windows: [Windows 10 support only](https://docs.docker.com/docker-for-windows/install/), и не все поставки
1. Docker Toolbox: [legacy](https://docs.docker.com/toolbox/overview/)
1. [Медленное монтирование из-за SMB](https://github.com/docker/for-win/issues/188)

## MacOS

1. [Медленное монтирование из-за osxfs](https://github.com/docker/for-mac/issues/77) [volume](https://docs.docker.com/glossary/?term=osxfs)
1. [hyperkit ate my CPU](https://github.com/docker/for-mac/issues/1759)

## Linux

1. Слишком
    1. Слишком старая версия докера в репозиториях: [ставить](https://docs.docker.com/install/linux/docker-ce/centos/) через репозитории Docker Inc или curl | bash
    1. Слишком новое ядро (Arch) [Unable to docker build on Linux kernel 4.19](https://github.com/docker/for-linux/issues/480), [тормозит](https://t.me/docker_ru/96193)
    1. Слишком старое ядро (CentOS) [Неправильно патчит файлы в AuFS](https://t.me/docker_ru/100652)
1. Не разрешаются адреса во время сборки/в контейнере, но `ping 8.8.8.8` работает: [Broken DNS](https://docs.docker.com/install/linux/linux-postinstall/#specify-dns-servers-for-docker)
1. Контейнер **сложно** запустить как сервис systemd, [лес костылей](https://github.com/moby/moby/issues/6791)
1. На диске занято слишком много места:

```
docker system df
docker system prune
docker system df
```
Если не помогло, то (**не повторять на проде!**)
```
systemctl stop docker
rm -rf /var/lib/docker
systemctl start docker
```

## Common
1. Не теряйте пароль от Docker Hub - [Reset Password Email Not Sending](https://github.com/docker/hub-feedback/issues/796)
1. Не используйте тэг `:latest`, [это анти-паттерн](https://vsupalov.com/docker-latest-tag/)

# Диагностика ошибок

## Исследуем контейнеры и образы

* `docker inspect dd8b322db23e | grep LABEL`
* `docker history` или [dive](https://github.com/wagoodman/dive)

![](https://pbs.twimg.com/media/DrboL-8WsAACDGz.jpg)


## Ошибки при запуске

Внимательно читайте сообщения об ошибках, они говорящие

Нет такого файла
```
$ docker run --rm alpine nginx
...
container_linux.go:344: starting container process caused "exec: \"nginx\": executable file not found in $PATH": unknown.
```

Монтирование файла поверх директории (или наоборот)
```
$ docker run --rm -ti -v /tmp:/bin/bash debian:9.5 sh
...
Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type.
```

Одноименный контейнер уже есть

```
$ docker run -d --name first nginx
...
The container name "/first" is already in use by container "7e07e06c812e09c5753dcbf4849a721f8c46840d0492b034c3cad963b9fcb315".
```

Неправильный порядок и/или синтаксис команд
```
$ docker run --rm alpine date; hostname
Sat Mar 16 10:04:32 UTC 2019
qwerty

$ docker run --rm alpine sh -c "date; hostname"
Sat Mar 16 10:04:47 UTC 2019
1bd26bcc4710
```

Контейнер запустился и сразу завершился == завершился процесс с PID=1. Почему не стартует контейнер `docker run --rm alpine sh`? Возможно, он ожидал интерактивного сеанса, `docker run -ti`

## Проблемы с сетью

Правило большого пальца:
1. если нужно обращаться в контейнер с хостовой машины - то пробрасывайте порты `run -p 8080:80`
1. если нужно обращаться из контейнера на хостовую машину - `run --network=host` или используйте внешний адрес машины

### Приложение не отвечает по сети

1. контейнер запущен, порты проброшены? `docker ps`
1. порт доступен, пингуется? `nc, ping, curl` с хоста
1. приложение принимает запросы на этом порту? принимает запросы с `0.0.0.0`? `nc, ping, curl` в контейнере

Типичная проверка доступности

```
$ docker run -d -p 80:80 nginx:alpine
dd8b322db23eb1

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                   NAMES
dd8b322db23e        nginx:alpine        "nginx -g 'daemon of…"   4 seconds ago       Up 1 second         127.0.0.1:80->80/tcp      modest_khorana

$ nc -z -w1 localhost 80; echo $?
0

$ docker exec -ti dd8b322db23e sh
\ # nc -z -w1 localhost 80; echo $?
0
\ # exit

$ curl -I localhost:80
HTTP/1.1 200 OK
...
```

Связать несколько контейнеров в сеть (удобнее работать через [`docker-compose`](https://docs.docker.com/compose/overview/))

```
docker run --name first nginx
docker run --name second --link first:nginx -ti sh

/ # ping nginx
PING nginx (172.17.0.3): 56 data bytes
64 bytes from 172.17.0.3: seq=0 ttl=64 time=0.147 ms
64 bytes from 172.17.0.3: seq=1 ttl=64 time=0.133 ms

/ # nc -z -w1 nginx 80; echo $?
0


/ # wget nginx
Connecting to nginx (172.17.0.3:80)
index.html
...
```

# Docker is not

* В докере плохо с безопасностью из коробки
    - [Understanding how uid and gid work in Docker containers](https://medium.com/@mccode/understanding-how-uid-and-gid-work-in-docker-containers-c37a01d01cf) vs [Isolate containers with a user namespace](https://docs.docker.com/engine/security/userns-remap/)
    - [S in Docker stands for Security](http://defcon-nn.ru/0x0A/012-stanislav.html) vs [Docker security](https://docs.docker.com/engine/security/security/)
* Докер не DNS, но можно поднять запустить [дополнительный контейнер](https://github.com/jwilder/nginx-proxy), который будет раздавать доменные имена. Хотите проще - правьте `/etc/hosts`
* Докер не виртуальная машина - контейнеры эфемерные, не нужно стараться их чинить - надо чинить исходный образ и пересоздавать контейнеры.


# Настройки, крутилки

## [daemon.json](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file) или [systemd...conf](https://docs.docker.com/config/daemon/systemd/#custom-docker-daemon-options)
- Подсетку, в которой раздавать IP адреса контейнерам
- Интерфейс, на котором публиковать порты (0.0.0.0 по умолчанию)
- явно указать DNS-сервера
- ...

## Drivers
- [Storage](https://docs.docker.com/storage/storagedriver/select-storage-driver/): OverlayFS, Btrfs, ZFS, VFS...
- [Logging](https://docs.docker.com/config/containers/logging/configure/): Journald, Syslog, JSON, GrayLog, Fluentd...
- [Machine](https://docs.docker.com/machine/drivers/): VirtualBox, MS Hyper-V, AWS, DO, Azure...

# Что дальше?

## Почитать
* [Get started](https://docs.docker.com/get-started/)
* [Habr: [docker]](https://habr.com/ru/search/?target_type=posts&q=%5Bdocker%5D&order_by=rating)
* [Docker для начинающего разработчика](https://blog.maddevs.io/docker-for-beginners-a2c9c73e7d3d)
* [Это будущее](https://habr.com/ru/post/276539/) :sarcasm:

## Попробовать
* [Katacoda: Learn Docker & Containers](https://www.katacoda.com/courses/docker/)
* [Play with Docker Classroom](https://training.play-with-docker.com/)
* [Stepik: Управление вычислениями(2 часть)](https://stepik.org/course/1612)

## Обсудить
[@docker_ru](https://t.me/docker_ru)

## Альтернативы
* [cri-o](https://cri-o.io/)
* [kata containers](https://katacontainers.io/)
* [gvisor](https://github.com/google/gvisor)

## Почитать про "overhead":
* [Another reason why your Docker containers may be slow](https://hackernoon.com/another-reason-why-your-docker-containers-may-be-slow-d37207dec27f)
* [Container isolation gone wrong](https://sysdig.com/blog/container-isolation-gone-wrong/)
* [IBM: An Updated Performance Comparison of Virtual Machines and Linux Containers - 2014](http://course.ece.cmu.edu/~ece845/docs/containers.pdf)

## Линтеры и сканеры
* [hadolint - Dockerfile linter, validate inline bash](https://github.com/hadolint/hadolint)
* [The Docker Bench for Security](https://github.com/docker/docker-bench-security)
* [Harbor -  registry project that stores, signs, and scans content](https://goharbor.io/)
