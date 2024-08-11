import React, { useCallback, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { v4 as uuidv4 } from 'uuid';
import ChatView from './ChatView'; // Assuming ChatView is in the same directory
import { Message, MessageCreateRequest } from '../../stores/ApiTypes';

import { client } from '../../stores/ApiClient';

// API functions
const fetchMessages = async (threadId: string): Promise<Message[]> => {
    const { data, error } = await client.GET('/api/messages/', { params: { query: { thread_id: threadId } } });
    if (error) {
        throw error;
    }
    return data.messages;
};

const sendMessage = async (message: MessageCreateRequest): Promise<Message> => {
    const { data, error } = await client.POST('/api/messages/', { body: message });
    if (error) {
        throw error;
    }
    return data;
};

const HelpChat: React.FC = () => {
    const [showMessages, setShowMessages] = useState(true);
    const [threadId, setThreadId] = useState<string>(uuidv4());
    const queryClient = useQueryClient();

    // Fetch messages
    const { data: messages = [] } = useQuery(['chatMessages', threadId], () => fetchMessages(threadId));

    // Send message mutation
    const mutation = useMutation(sendMessage, {
        onSuccess: (newMessage) => {
            queryClient.setQueryData(['chatMessages', threadId], (oldMessages: Message[] | undefined) =>
                [...(oldMessages || []), newMessage]
            );
        },
    });

    const handleSendMessage = useCallback(async (prompt: string) => {
        const messageRequest: MessageCreateRequest = {
            thread_id: threadId,
            role: 'user',
            content: prompt,
        };
        await mutation.mutateAsync(messageRequest);
    }, [threadId, mutation]);

    const resetThread = () => {
        const newThreadId = uuidv4();
        setThreadId(newThreadId);
        queryClient.setQueryData(['chatMessages', newThreadId], []);
    };

    return (
        <div className="help-chat">
            <h2>Software Help Chat</h2>
            <button onClick={resetThread}>Start New Chat</button>
            <ChatView
                messages={messages}
                showMessages={showMessages}
                setShowMessages={setShowMessages}
                sendMessage={handleSendMessage}
            />
        </div>
    );
};

export default HelpChat;