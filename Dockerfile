FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    python3-dev \
    python3-pip \
    vim \
    npm

RUN npm install -g less
RUN mkdir /var/run/sshd
RUN echo 'root:asd' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN echo "alias python=/usr/bin/python3" >> /etc/profile
RUN echo "alias recipes=/var/recipes/lazymeals" >> /etc/profile

COPY / /var/recipes/
WORKDIR /var/recipes

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]