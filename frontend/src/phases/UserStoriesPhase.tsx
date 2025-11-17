import { useLocation } from "react-router-dom";
import { ProjectRequirements, UserStories } from "../types";
import React, { useState } from "react";
import Loading from "../components/Loading";

export default function UserStoriesPhase() {
  const location = useLocation();
  const data = location.state?.data;
  const [loading, setLoading] = useState(true);
  //   const requirements = location.state?.requirements as UserStories;

  const [userStories, setUserStories] = useState<UserStories>({
    messages: [],
    user_stories: [],
  });

  React.useEffect(() => {
    // console.log(data.user_stories)
    // console.log(data.user_stories[0].story_id)
    // console.log(location.state?.["user-stories"].user_stories)
    setLoading(true)
    if (location.state?.["user-stories"]?.user_stories) {
      console.log("inside")
      setUserStories(prevState => ({
        ...prevState,
        user_stories: location.state?.["user-stories"].user_stories,
      }))
      setLoading(false)
      return
    }
    if (data.user_stories) {
      setUserStories(prevState => ({
        ...prevState,
        user_stories: [...prevState.user_stories, ...data.user_stories],
      }))
      setLoading(false)
    }
    // console.log(userStories.user_stories)
  }, [location.state])
  const badgeColors = [
    "bg-blue-900/50 text-blue-300",
    "bg-green-900/50 text-green-300",
    "bg-purple-900/50 text-purple-300",
    "bg-amber-900/50 text-amber-300",
    "bg-pink-900/50 text-pink-300",
    "bg-teal-900/50 text-teal-300",
  ];

  if(loading) {
    return <Loading />;
  }

  return (
    <div className="flex-1 p-6 overflow-y-auto bg-gray-900">
      <div className="max-w-6xl mx-auto">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <div className="border-b border-gray-700 pb-6 mb-6">
            <h3 className="text-2xl font-bold text-white mb-2">
              User Story Phase
            </h3>
            <p className="text-gray-400">
              These user stories define the functionality of your application
              from the perspective of the user.
            </p>
          </div>

          <div className="space-y-6">
            {userStories.user_stories.map((userStory, index) => {
              const colorClass = badgeColors[index % badgeColors.length];
              return (
                <div
                  key={userStory.story_id}
                  className={`bg-gradient-to-br from-gray-800 to-gray-700 rounded-2xl shadow-xl border border-gray-600 hover:scale-[1.01] transition-transform duration-300 ease-in-out`}
                >
                  <div className="grid md:grid-cols-2 gap-0">
                    {/* Left side - User Story Details */}
                    <div className="p-6 border-b md:border-b-0 md:border-r border-gray-600 space-y-4">
                      <div className="flex items-center gap-2">
                        <span
                          className={`text-xs font-bold uppercase tracking-wide  px-3 py-1 rounded-full  ${colorClass}`}
                        >
                          {userStory.story_id}
                        </span>
                      </div>
                      <h4 className="text-2xl font-bold text-white">
                        {userStory.title}
                      </h4>
                      <p className="text-gray-300 leading-relaxed text-sm">
                        {userStory.description}
                      </p>
                    </div>

                    {/* Right side - Acceptance Criteria */}
                    <div className="p-6 bg-gray-800/50 space-y-4">
                      <h4 className="text-lg font-semibold text-white">
                        Acceptance Criteria
                      </h4>
                      <ul className="space-y-2">
                        {userStory.acceptance_criteria.map(
                          (criteria, index) => (
                            <li
                              key={index}
                              className="flex items-start gap-3 text-gray-300 text-sm"
                            >
                              <span className="text-blue-400">•</span>
                              <span>{criteria}</span>
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
