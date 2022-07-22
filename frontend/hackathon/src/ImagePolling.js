


import React, { useEffect, useState } from "react";

export default function ImagePolling() {
  const [answer, setAnswer] = useState();

  const getAnswer = async () => {
    const res = await fetch("http://127.0.0.1:5000/uploaded-images");
    const data = await res.json();
    setAnswer(data);
  };

  useEffect(() => {
    const timer = setInterval(getAnswer, 2000);
    return () => clearInterval(timer);
  }, []);

  if (!answer?.original) {
    return <div></div>
  }
  const zip = (a, b) => a.map((k, i) => [k, b[i]]);
  const result = zip(answer.original, answer.modified)
  return <div>{result.map((elem, index) => {
    return <div> <img src={`data:image/jpeg;base64,${answer.original[index]}`} /><img src={`data:image/jpeg;base64,${answer.modified[index]}`} /></div>
  })}</div>

  // return <div></div>
  return <div>{answer.original.map(elem => {
    return <img src={`data:image/jpeg;base64,${elem}`} />
  })}{answer.modified.map(elem => {
    return <img src={`data:image/jpeg;base64,${elem}`} />
  })}</div>;
}

