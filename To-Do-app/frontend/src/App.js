useEffect(() => {
    fetch('http://<EC2_PUBLIC_IP>:5000/todos')
      .then(res => res.json())
      .then(data => setTodos(data));
  }, []);