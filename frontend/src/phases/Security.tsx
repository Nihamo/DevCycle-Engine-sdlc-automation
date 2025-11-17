import React, { useState } from "react"
import { useLocation } from "react-router-dom"
import { SecurityReview } from "../types";
import { BACKEND_URL } from "../../config";
import SecurityReviewCard from "../components/SecurityReviewCard";
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";

export default function Security() {


    const location = useLocation();
    const data = location.state?.data;
    const [loading, setLoading] = useState(true);

    const [securityReviewData, setSecurityReviewData] = useState<SecurityReview>({
        reviews: [],
    })


    const getSecurityReviewData = async () => {
        setLoading(true);
        if (location.state?.["security"]?.reviews) {
            console.log("security inside");
            setSecurityReviewData({
                reviews: location.state?.["security"].reviews,
            })
            setLoading(false);
            return
        }
        try {
            console.log("security outside")
            if (!data?.session_id) {
                throw new Error("Session ID is missing");
            }

            const response = await fetch(`${BACKEND_URL}/security/review/get/${data.session_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("failed to call /security/review/get/{{session_id}}")
            }

            const security_review_response = await response.json();
            // console.log(security_review_response.reviews)
            setSecurityReviewData({
                reviews: security_review_response.reviews,
            })
            setLoading(false);

        } catch (error) {
            console.error("error calling /security/review/get/{{session_id}}")
            setLoading(false);
            ToastError(error)
        }
    }

    React.useEffect(() => {
        if (data) {
            getSecurityReviewData()
        }
    }, [location.state])

    if (loading) {
        return <Loading />
    }


    const getPriorityColor = (priority: string) => {
        switch (priority.toLowerCase()) {
            case "high":
                return {
                    box: "from-red-950 via-red-900 to-red-800",
                    smallBox: "bg-red-950",
                    badge: "bg-red-200 text-red-600",
                    text: "text-red-200",
                    line: "border-red-400",
                };
            case "medium":
                return {
                    box: "from-yellow-950 via-yellow-900 to-yellow-800",
                    smallBox: "bg-yellow-950",
                    badge: "bg-yellow-200 text-yellow-600",
                    text: "text-yellow-200",
                    line: "border-yellow-400",
                };
            case "low":
                return {
                    box: "from-green-950 via-green-900 to-green-800",
                    smallBox: "bg-green-950",
                    badge: "bg-green-200 text-green-600",
                    text: "text-green-200",
                    line: "border-green-400",
                };
            default:
                return {
                    box: "from-gray-950 via-gray-900 to-gray-800",
                    smallBox: "bg-gray-950",
                    badge: "bg-gray-200 text-gray-600",
                    text: "text-gray-200",
                    line: "border-gray-400",
                };
        }
    }

    return (
        <div
            className="flex-1 p-6 overflow-y-auto bg-gray-900"
        >
            <div className="max-w-6xl mx-auto px-2">
                <p className="text-xl font-semibold">Security Review</p>
                <p className="text-sm pt-1 text-gray-400 font-medium">Security analysis of the generated code to identify potential vulnerabilities.</p>
            </div>
            <div className="max-w-6xl py-6 mx-auto">
                <div className="bg-gray-700 rounded-lg shadow-xl p-5 border border-gray-400">
                    <div className="flex flex-col">
                        <p
                            className="text-xl font-bold text-gray-100"
                        >
                            Vulnerabilities
                        </p>
                        <div className="py-4 flex flex-col gap-6">
                            {securityReviewData.reviews && securityReviewData.reviews.map((review, index) => {

                                const priorityStyle = getPriorityColor(review.priority);
                                return (
                                    <SecurityReviewCard
                                        key={index}
                                        review={review}
                                        priorityStyle={priorityStyle}
                                    />
                                )
                            })}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}