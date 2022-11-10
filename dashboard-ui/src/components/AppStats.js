import React, {useEffect, useState} from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

    const getStats = () => {

        fetch(`http://acit-3855-kafka.jake-m-commits.link:8100/stats`)
            .then(res => res.json())
            .then((result) => {
                console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            }, (error) => {
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
        const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
        return () => clearInterval(interval);
    }, [getStats]);

    if (error) {
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false) {
        return (<div>Loading...</div>)
    } else if (isLoaded === true) {
        return (
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
                    <tbody>
                        <tr>
                            <th>Answers</th>
                            <th>Questions</th>
                        </tr>
                        <tr>
                            <td># A: {stats['num_answers']}</td>
                            <td># Q: {stats['num_questions']}</td>
                        </tr>
                        <tr>
                            <td colspan="2">max_randInt_answers: {stats['max_randInt_answers']}</td>
                        </tr>
                        <tr>
                            <td colspan="2">max_randInt_questions: {stats['max_randInt_questions']}</td>
                        </tr>
                    </tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
