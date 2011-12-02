<?php

class ZeroMQMessagePackClient
{
	private $_socket;

	public static function construct($uri)
	{
		return new self($uri);
	}

	public function __construct($uri)
	{
		/* Create new queue object */
		$this->_socket = new ZMQSocket(
			new ZMQContext(),
			ZMQ::SOCKET_PUB,
			'socket1'
		);

		$this->_socket->connect($uri);
	}

	public function send($error)
	{
		$this->_socket->send($this->_pack($error), ZMQ::MODE_NOBLOCK);
	}

	private function _pack($data)
	{
		$msgPack = new MessagePack();
		return $msgPack->pack($data);
	}
}

class TriageClient extends ZeroMQMessagePackClient
{
	public function logError($error)
	{
		$this->send(array(
				'error' => $error,
				'time' => time()
			));

		return $this;
	}

	public function logMessage($level, $message)
	{
		$this->send(array(
				'message' => $message,
				'level' => $level,
				'time' => time()
			));

		return $this;
	}
}

$client = new TriageClient('tcp://10.0.1.32:5001');

