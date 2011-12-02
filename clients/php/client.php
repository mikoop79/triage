<?php

/*
The client sends two messages using two different sockets
and then exits
*/

/* Create new queue object */
$queue = new ZMQSocket(new ZMQContext(), ZMQ::SOCKET_REQ);
$queue->connect("tcp://10.0.1.33:5000");
//$queue->connect("tcp://127.0.0.1:5555");

echo "sending hello there... \n\n";

$send = $queue->send("hello there..!");

echo "waiting for response...\n\n";

/* Assign socket 1 to the queue, send and receive */
var_dump($send->recv());

echo "sending complete";
