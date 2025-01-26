import { ActivityIndicator, ScrollView, Text, View } from "react-native";
import { useEffect, useState } from "react/cjs/react.production.min";
import APIs, { endpoints } from "../../configs/APIs";
import MyStyles from "../../styles/MyStyles";
import React from 'react'
import Items from "./Items";

const Room = ({ route }) => {
    const roomId = route.params?.roomId;
    const [room, setRoom] = React.useState(null);

    const loadRoom = async () => {
        let res = await APIs.get(endpoints['room'](courseId));
        setRoom(res.data);
    }

    React.useEffect(() => {
        loadRoom();
    }, [roomId]);

    return (
        <ScrollView>
            {room===null?<ActivityIndicator />:<>
                {room.map(le => <Items key={le.id} item={le} routeName='roomDetails' params={{'roomId': le.id}} />)}
            </>}
        </ScrollView>
    );
}

export default Room;