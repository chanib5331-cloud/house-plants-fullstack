import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './plantDetail.css';



function PlantDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [plant, setPlant] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(`http://localhost:8001/plants/${id}`)
            .then((response) => {
                setPlant(response.data);
                setLoading(false);
            })
            .catch((error) => {
                console.error(error);
                setLoading(false);
            });
    }, [id]);

    if (loading) {
        return <div className="loading-container">Loading...</div>;
    }


    return (
        <div className="plant-detail-container">
            <button className="back-button" onClick={() => navigate('/')}>
                ← Back to Plants
            </button>
            <div className="plant-detail-card">
                <h1 className="plant-title">{plant["Latin name"] || 'N/A'}</h1>

                <div className="plant-details">
                    {Object.entries(plant)
                        .filter(([key]) => key !== "Latin name" && key !== "Img")
                        .map(([key, value]) => (
                            <PlantInfo key={key} label={key} value={value} />
                        ))
                    }
                    {plant["Img"] && <img className="plant-image" src={plant["Img"]} alt={plant["Latin name"]} />}
                </div>
            </div>
        </div>
    )
}

export default PlantDetail;

function PlantInfo({ label, value }) {
    return <p className="plant-info">{label}: {value} </p>;
}