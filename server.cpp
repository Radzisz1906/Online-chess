#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <fcntl.h>  // for open
#include <unistd.h> // for close
#include <pthread.h>
#include <iostream>
#include <string>

char client_message[2000];
char buffer[1024];
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

int watki[1024][3];

struct game
{
  int player1 = 0;
  int player2 = 0;
  int p = 0;
  int d = 0;
  int turnone = 1;
  int turntwo = 0;
  char last[10] = "Nic";
};

game gry[1024];

void *socketThread(void *arg)
{
  printf("new thread \n");
  int newSocket = *((int *)arg);
  int n;
  for (;;)
  {
    char msg[1024] = "1.Stworz pokoj.\n2.Dolacz do pokoju\n";
    char *message = (char *)malloc(strlen(msg));
    strcpy(message, msg);
    sleep(1);
    send(newSocket, message, strlen(message), 0);
    free(message);

    n = recv(newSocket, client_message, 2000, 0);

    printf("Wiadomosc: %s\n", client_message);
    int id;
    int opcja;
    int ruch;
    opcja = std::atoi(client_message);
    printf("ID: %i\n", id);
    if (opcja == 1)
    {
      strcpy(msg, "Podaj id gry (od 1 do 1023)!");
      message = (char *)malloc(strlen(msg));
      strcpy(message, msg);
      sleep(1);
      send(newSocket, message, strlen(message), 0);
      free(message);
      n = recv(newSocket, client_message, 2000, 0);
      printf("Wiadomosc: %s\n", client_message);
      id = std::atoi(client_message);
      printf("ID: %i\n", id);
      memset(&client_message, 0, strlen(client_message));
      if (id > 0 && gry[id].player1 == 0)
      {
        strcpy(msg, "Stworzyles pokoj!");
        message = (char *)malloc(strlen(msg));
        strcpy(message, msg);
        sleep(1);
        send(newSocket, message, strlen(message), 0);
        free(message);
        gry[id].player1 = 1;
        while (gry[id].player2 == 0)
        {
        }
        strcpy(msg, "Gra");
        message = (char *)malloc(strlen(msg));
        strcpy(message, msg);
        sleep(1);
        send(newSocket, message, strlen(message), 0);
        free(message);
        while (gry[id].p == 0 && gry[id].d == 0)
        {
          if (gry[id].turnone == 1)
          {
            strcpy(msg, "Twoj ruch!");
            message = (char *)malloc(strlen(msg));
            strcpy(message, msg);
            sleep(1);
            send(newSocket, message, strlen(message), 0);
            free(message);
            strcpy(msg, gry[id].last);
            message = (char *)malloc(strlen(msg));
            strcpy(message, msg);
            sleep(1);
            send(newSocket, message, strlen(message), 0);
            free(message);
            n = recv(newSocket, client_message, 2000, 0);
            strcpy(gry[id].last, client_message);
            ruch = std::atoi(client_message);
            memset(&client_message, 0, strlen(client_message));
            gry[id].turntwo = 1;
            gry[id].turnone = 0;
          }
        }
      }
      else
      {
        strcpy(msg, "Zle id!");
        message = (char *)malloc(strlen(msg));
        strcpy(message, msg);
        sleep(1);
        send(newSocket, message, strlen(message), 0);
        free(message);
      }
    }
    else if (opcja == 2)
    {
      strcpy(msg, "Podaj id gry (od 1 do 1023)!");
      message = (char *)malloc(strlen(msg));
      strcpy(message, msg);
      sleep(1);
      send(newSocket, message, strlen(message), 0);
      free(message);
      n = recv(newSocket, client_message, 2000, 0);
      id = std::atoi(client_message);

      memset(&client_message, 0, strlen(client_message));
      if (id > 0 && gry[id].player1 == 1 && gry[id].player2 == 0)
      {
        strcpy(msg, "Dolaczyles do pokoju!");
        message = (char *)malloc(strlen(msg));
        strcpy(message, msg);
        sleep(1);
        send(newSocket, message, strlen(message), 0);
        free(message);
        gry[id].player2 = 1;
        strcpy(msg, "Gra");
        message = (char *)malloc(strlen(msg));
        strcpy(message, msg);
        sleep(1);
        send(newSocket, message, strlen(message), 0);
        free(message);
        while (gry[id].p == 0 && gry[id].d == 0)
        {
          if (gry[id].turntwo == 1)
          {
            strcpy(msg, "Twoj ruch!");
            message = (char *)malloc(strlen(msg));
            strcpy(message, msg);
            sleep(1);
            send(newSocket, message, strlen(message), 0);
            free(message);
            strcpy(msg, gry[id].last);
            message = (char *)malloc(strlen(msg));
            strcpy(message, msg);
            sleep(1);
            send(newSocket, message, strlen(message), 0);
            free(message);
            n = recv(newSocket, client_message, 2000, 0);
            strcpy(gry[id].last, client_message);
            ruch = std::atoi(client_message);
            memset(&client_message, 0, strlen(client_message));
            gry[id].turntwo = 0;
            gry[id].turnone = 1;
          }
        }
      }
      else
      {
        strcpy(msg, "Zle id!");
        message = (char *)malloc(strlen(msg));
        strcpy(message, msg);
        sleep(1);
        send(newSocket, message, strlen(message), 0);
        free(message);
      }
    }
    else
    {
      strcpy(msg, "0");
      message = (char *)malloc(strlen(msg));
      strcpy(message, msg);
      sleep(1);
      send(newSocket, message, strlen(message), 0);
      memset(&client_message, 0, strlen(client_message));
      free(message);
    }

    // printf("Exit socketThread \n");
    //
    // pthread_exit(NULL);
  }
  printf("Exit socketThread \n");

  pthread_exit(NULL);
}

int main()
{

  int serverSocket, newSocket;
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  socklen_t addr_size;

  // Create the socket.
  serverSocket = socket(PF_INET, SOCK_STREAM, 0);

  // Configure settings of the server address struct
  // Address family = Internet
  serverAddr.sin_family = AF_INET;

  // Set port number, using htons function to use proper byte order
  serverAddr.sin_port = htons(8080);

  // Set IP address to localhost
  serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

  // Set all bits of the padding field to 0
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

  // Bind the address struct to the socket
  bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr));

  // Listen on the socket
  if (listen(serverSocket, 50) == 0)
    printf("Listening\n");
  else
    printf("Error\n");
  pthread_t thread_id;

  while (1)
  {
    // Accept call creates a new socket for the incoming connection
    addr_size = sizeof serverStorage;
    newSocket = accept(serverSocket, (struct sockaddr *)&serverStorage, &addr_size);

    if (pthread_create(&thread_id, NULL, socketThread, &newSocket) != 0)
      printf("Failed to create thread\n");

    pthread_detach(thread_id);
    // pthread_join(thread_id,NULL);
  }
  return 0;
}
