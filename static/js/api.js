
async function get_id() {
  try {
    const response = await fetch("/api/self_id");
    const data = await response.json();
    return data
  } catch (err) {
    console.error(err);
    return [];
  }
}

async function get_user_info(id) {
  try {
    const response = await fetch(`/api/user_info/${id}`);
    const data = await response.json();
    return data
  } catch (err) {
    console.error(err);
    return [];
  }
}


async function get_user_list() {
    try {
        const response = await fetch("/api/users");
        const data = await response.json();
        // console.log(data);
        return data;
    } catch (err) {
        console.error(err);
        return [];
    }
}

async function get_received_messages() {
    try {
      const response = await fetch(`/api/received_messages`);
      const data = await response.json();
      // console.log(data);
      return data;
    } catch (err) {
      console.error(err);
      return [];
    }
}

async function get_sent_messages() {
    try {
      const response = await fetch(`/api/sent_messages`);
      const data = await response.json();
      // console.log(data);
      return data;
    } catch (err) {
      console.error(err);
      return [];
    }
}


async function get_received_messages_from(sender_id) {
    try {
      const response = await fetch(`/api/received_messages/${sender_id}`);
      const data = await response.json();
      // console.log(data);
      return data;
    } catch (err) {
      console.error(err);
      return [];
    }
}

async function get_sent_messages_to(receiver_id) {
    try {
      const response = await fetch(`/api/sent_messages/${receiver_id}`);
      const data = await response.json();
      // console.log(data);
      return data;
    } catch (err) {
      console.error(err);
      return [];
    }
}

async function get_similar_messages(other_id) {
  try {
    const response = await fetch(`/api/related_messages/${other_id}`);
    const data = await response.json();
    // console.log(data);
    return data;
  } catch (err) {
    console.error(err);
    return [];
  }
}